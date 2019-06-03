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
        # containers:
        pump_figure_cont = self.builder.get_object('Frame_Pump_Figure')
        pipe_figure_cont = self.builder.get_object('Frame_Pipe_Figure')
        station_figure_cont = self.builder.get_object('Frame_Station_Figure')
        report_figure_cont = self.builder.get_object('Frame_Report_Figure')
        # setting figures dimensions
        self.pump_figure, self.pump_plot, self.pump_canvas = figs.init_figure(
            pump_figure_cont, 5.1, 4.6)
        self.pipe_figure, self.pipe_plot, self.pipe_canvas = figs.init_figure(
            pipe_figure_cont, 8.4, 3.8)
        self.stat_figure, self.stat_plot, self.stat_canvas = figs.init_figure(
            station_figure_cont, 4.5, 4.7)
        self.rep_figure, self.rep_plot, self.rep_canvas = figs.init_figure(
            report_figure_cont, 4.65, 6.0)
        # setting placement
        self.pump_canvas.get_tk_widget().grid(row=0, column=0)
        self.pipe_canvas.get_tk_widget().grid(row=0, column=0)
        self.stat_canvas.get_tk_widget().grid(row=0, column=0)
        self.rep_canvas.get_tk_widget().grid(row=0, column=0)

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

        nbook = self.builder.get_object('Notebook_Data')
        if mode == 'checking':
            nbook.tab(3, state='disabled')
            nbook.tab(4, state='disabled')
        elif mode == 'minimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='disabled')
        elif mode == 'optimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='normal')
        log.info('changed mode: {0}'.format(mode))

    def ui_set_shape(self):
        """ Function changing shape setting, triggered by user interaction.
        Gets present setting, and sets its in station object
        """
        shape = self.ui_vars.__getitem__('shape').get()
        self.station.well.set_shape(shape)

    def run(self):
        """ Makes infinite loop
        """
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
