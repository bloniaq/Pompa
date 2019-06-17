import tkinter as tk  # for python 3
import pygubu
import logging

# import modules
import models.data as data
import models.variables as variables
import models.station as station
import models.well as well
import models.pump as pump
import models.pipe as pipe
import view.figures as figs
import view.view as view
import view.report as report
import calculation as calc

# LOGGING CONFIG

log = logging.getLogger()
log.handlers = []

log = logging.getLogger('pompa')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('logfile.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s-%(name)s-%(levelname)s: %(message)s',
    datefmt='%H:%M:%S')

ch.setFormatter(formatter)
fh.setFormatter(formatter)

log.addHandler(ch)
log.addHandler(fh)


# MAIN APP CLASS

class Application():

    def __init__(self):

        # 1: Create a builder
        self.builder = pygubu.Builder()

        # 2: Load an ui file
        self.builder.add_from_file('view\\pompa_gui.ui')

        # 3: Defining important widgets and handlers
        self.mainwindow = self.builder.get_object('Toplevel_Main')
        self.filepath = self.builder.get_object('filepath')
        self.ui_vars = self.builder.tkvariables

        # 4: Setting callbacks
        self.builder.connect_callbacks(self)

        # 5: creating model objects
        self.init_models()

        variables.Variable.load_flag = False

        self.init_figures()

    def init_models(self):
        """ Returns nothing

        Initialize model objects, and binds them to controller"
        """

        self.mode = variables.Logic(self, 'checking', 'mode', '1',
                                    data.dan_mode, self.ui_set_mode)
        self.ui_set_mode()

        self.station = station.Station(self)
        data.station_vars(self)

        self.station.well = well.Well(self)
        data.well_vars(self)
        self.ui_set_shape()

        self.station.pump = pump.PumpType(self)
        data.pump_vars(self)
        self.station.pump.set_flow_unit(
            self.ui_vars.__getitem__('pump_flow_unit').get())

        self.station.ins_pipe = pipe.Pipe(self)
        data.ins_pipe_vars(self)

        self.station.out_pipe = pipe.Pipe(self)
        data.out_pipe_vars(self)

    def init_figures(self):
        """ Returns nothing

        Initialize objects for carrying figures
        """

        # setting figures dimensions
        self.pump_fig = figs.PumpFig(self, self.builder.get_object(
            'Frame_Pump_Figure'), 5.1, 4.6)

        self.pipe_fig = figs.PipeFig(self, self.builder.get_object(
            'Frame_Pipe_Figure'), 8.4, 3.8)

        self.report_fig = figs.ReportFig(self, self.builder.get_object(
            'Frame_Report_Figure'), 4.65, 6.0)

        self.schema = figs.Schema(self, self.builder.get_object(
            'Frame_Station_Figure'), 4.5, 4.7)

        # setting placement
        self.pump_fig.canvas.get_tk_widget().grid(row=0, column=0)
        self.pipe_fig.canvas.get_tk_widget().grid(row=0, column=0)
        self.schema.canvas.get_tk_widget().grid(row=0, column=0)
        self.report_fig.canvas.get_tk_widget().grid(row=0, column=0)

    def load_data(self):
        """ Returns nothing

        Gets filename from widget, reckongizes save version, and loads data
        """
        log.info('\ndata_load started\n')
        global path
        path = self.filepath.cget('path')
        log.debug('path: {}'.format(path))
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n\n'.format(str(file)))
            first_line = file.readline()
            # Checking if 1.0 version
            if first_line[0] == '1' and first_line[1] == ')':
                data_dictionary = data.get_data_dict_from_dan_file(path)
        self.station.load_data(data_dictionary)
        self.station.well.load_data(data_dictionary)
        self.station.ins_pipe.load_data(data_dictionary)
        self.station.out_pipe.load_data(data_dictionary)
        self.station.pump.load_data(data_dictionary)

        self.builder.get_object('Text_Report').delete('1.0', tk.END)
        # Updating Figures

        # poprawić odświeżanie wykresów

        self.draw_auxillary_figures("pipe_char", "pump_char")

    def ui_set_mode(self):
        """ Changing mode of work. Triggered by user interaction. Gets present
        setting from a widget, and sets it in station object
        """
        self.set_mode(self.ui_vars.__getitem__('mode').get())

    def set_mode(self, mode):
        """ Function sets some widgets properities, according to present work
        mode setting
        """
        self.mode.value = mode
        view.set_mode(self.builder, mode)

    def ui_set_shape(self):
        """ Function changing shape setting, triggered by user interaction.
        Gets present setting, and sets its in station object
        """
        shape = self.ui_vars.__getitem__('shape').get()
        self.set_shape(shape)

    def set_shape(self, shape):
        self.station.well.shape.value = shape
        view.set_shape(self.builder, self.ui_vars, shape)

    def set_pump_flow_unit(self):
        """ Function reacts on a pump flow unit setting, and runs a method of
        pump type object, and updates the figure
        """
        log.info('set_pump_flow_unit started')
        current_setting = self.ui_vars.__getitem__('pump_flow_unit').get()
        self.pump_type.set_flow_unit(current_setting)
        log.debug('going to draw figure')
        self.draw_pump_figure()

    def set_inflow_unit(self):
        """ Function updates proper figure
        """
        self.draw_pipe_figure()

    def pump_get_coords(self):
        """ Function run by using Add Point button. Starts by getting values
        from widgets, and pass them to pump type method, then it updates figure
        """
        log.info('get_coords started')
        flow_entry = self.builder.get_object('Entry_Add_char_point_flow')
        flow_value = flow_entry.get()
        flow_entry.delete(0, 'end')
        lift_entry = self.builder.get_object('Entry_Add_char_point_lift')
        lift_value = lift_entry.get()
        lift_entry.delete(0, 'end')
        self.pump_type.characteristic.add_point(flow_value, lift_value)
        self.pump_type.characteristic.sort_points()
        self.draw_pump_figure()

    def pump_delete_point(self):
        """ Function run by using Delete Point button. Gets id of focused point
        and pass it to pump type method, then updates figure
        """
        log.info('pump_delete_button started')
        deleted_id = self.pump_type.characteristic.tree.focus()
        if deleted_id != '':
            self.pump_type.characteristic.delete_point(deleted_id)
        self.draw_pump_figure()

    def interp(self, wanted_x, x_arr, y_arr):
        return calc.interp(wanted_x, x_arr, y_arr)

    def fit_coords(self, xcoords, ycoords, degree):
        return calc.fit_coords(xcoords, ycoords, degree)

    def work_point(self, pump, pipes):
        return calc.work_point(pump, pipes)

    def draw_report_figure(self):
        # TODO is this function needed?
        self.report_fig.update()

    def draw_pipe_figure(self):
        # TODO is this function needed?
        self.pipe_fig.update()

    def draw_pump_figure(self):
        # TODO is this function needed?
        self.pump_fig.update()

    def draw_schema(self):
        # TODO is this function needed?
        self.schema.update()

    def draw_auxillary_figures(self, *figures):
        # TODO is this function needed?

        dependencies = {"pipe_char": self.draw_pipe_figure(),
                        "pump_char": self.draw_pump_figure(),
                        "schema": self.draw_schema()}

        for figure in figures:
            dependencies[figure]

    def show_report(self, report):
        # TODO is this function needed?
        text_container = self.builder.get_object('Text_Report')
        text_container.delete('1.0', tk.END)
        text_container.insert('1.0', report)

    def calculate(self):

        # ma wskazywać na moduł calculation
        validation = self.station.calculate(self.mode.value)
        if validation:
            report_content = report.Report(self.station)
            self.show_report(report_content.convert_to_string())

        pass

    def run(self):
        """ Makes infinite loop
        """
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
