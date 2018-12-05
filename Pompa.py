import tkinter as tk  # for python 3
'''
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
'''
import pygubu
import logging
import numpy as np

import classes
import maths
import data

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

variables_list = []
path = ""

# LOGGING CONFIGURATION

# clearing root logger handlers
log = logging.getLogger()
log.handlers = []

# setting new logger
log = logging.getLogger('Pompa')
log.setLevel(logging.DEBUG)

# create console and file handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('logfile.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s-%(name)s-%(levelname)s: %(message)s',
    datefmt='%H:%M:%S')

#    datefmt='%Y.%m.%d %H:%M:%S')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)
log.addHandler(fh)


class Application():

    dan_mode = {'0': 'minimalisation', '1': 'checking', '2': 'optimalisation'}
    default = data.default

    def __init__(self):

        # 1: Create a builder
        self.builder = pygubu.Builder()

        # 2: Load an ui file
        self.builder.add_from_file('GUI_Pygubu.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = self.builder.get_object('Toplevel_Main')
        self.filepath = self.builder.get_object('filepath')
        self.ui_vars = self.builder.tkvariables

        fcontainer = self.builder.get_object('Frame_Chart')

        self.figure = fig = Figure(figsize=(4.2, 5.1), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=fcontainer)
        canvas.get_tk_widget().grid(row=0, column=0)

        # 4: Setting callbacks
        self.builder.connect_callbacks(self)

        # 5: creating objects

        self.create_objects()
        self.set_mode(self.default['mode'])

    def run(self):
        self.mainwindow.mainloop()

    def create_objects(self):
        self.well = classes.Well(self)
        data.well_vars(self.well, self)
        self.pump = self.well.pump = classes.PumpType(self)
        data.pump_vars(self.pump, self)
        self.pump.set_flow_unit(
            self.ui_vars.__getitem__('pump_flow_unit').get())
        self.discharge_pipe = self.well.discharge_pipe = classes.Pipe(self)
        data.discharge_pipe_vars(self.discharge_pipe, self)
        self.collector = self.well.collector = classes.Pipe(self)
        data.collector_vars(self.collector, self)

    def load_data(self):
        log.info('\ndata_load started\n')
        global path
        path = self.filepath.cget('path')
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n\n'.format(str(file)))
            # rozpoznaj plik
            first_line = file.readline()
            # rozpoznanie wersji zapisu
            if first_line[0] == '1' and first_line[1] == ')':
                data_dictionary = self.dan_data_dictionary(path)
        self.well.load_data(data_dictionary)
        self.discharge_pipe.load_data(data_dictionary)
        self.collector.load_data(data_dictionary)
        self.pump.load_data(data_dictionary)
        self.draw_figure()

    def dan_data_dictionary(self, path):
        log.info('\ndan_load started\n')
        log.info('plik danych generowany wersją 1.0 aplikacji')
        data_dictionary = {}
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n\n'.format(str(file)))
            for line in file:
                id_line, line_datas = line.split(')')
                line_datas_list = line_datas.split()
                stored_value = line_datas_list[0]
                log.debug('id: {}, stored value: {}'.format(
                    id_line, stored_value))
                if id_line not in data_dictionary:
                    data_dictionary[id_line] = []
                data_dictionary[id_line].append(stored_value)
                log.debug('dan_id: {}, value: {}'.format(
                    id_line, data_dictionary[id_line]))
            log.debug('dictionary in progress: {}'.format(data_dictionary))
            for id_ in data_dictionary:
                if len(data_dictionary[id_]) == 1:
                    data_dictionary[id_] = data_dictionary[id_][0]
                    data_dictionary[id_] = float(data_dictionary[id_])
                    # expand for exceptions, make floats
                else:
                    data_dictionary[id_] = [float(s)
                                            for s in data_dictionary[id_]]
            log.debug('dictionary at finish: {}'.format(data_dictionary))
            return data_dictionary

    def ui_set_shape(self):
        shape = self.ui_vars.__getitem__('shape').get()
        self.well.set_shape(shape)

    def ui_set_mode(self):
        mode = self.ui_vars.__getitem__('mode').get()
        self.set_mode(mode)

    def set_mode(self, mode):
        ''' changes application mode
        '''
        self.ui_vars.__getitem__('mode').set(mode)
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

    def set_pump_flow_unit(self):
        log.info('set_pump_flow_unit started')
        current_setting = self.ui_vars.__getitem__('pump_flow_unit').get()
        self.pump.set_flow_unit(current_setting)
        log.debug('going to draw figure')
        self.draw_figure()

    def pump_get_coords(self):
        log.info('get_coords started')
        flow_entry = self.builder.get_object('Entry_Add_char_point_flow')
        flow_value = flow_entry.get()
        flow_entry.delete(0, 'end')
        lift_entry = self.builder.get_object('Entry_Add_char_point_lift')
        lift_value = lift_entry.get()
        lift_entry.delete(0, 'end')
        self.pump.characteristic.add_point(flow_value, lift_value)
        self.pump.characteristic.sort_points()
        self.draw_figure()

    def pump_delete_point(self):
        log.info('pump_delete_button started')
        deleted_id = self.pump.characteristic.tree.focus()
        if deleted_id != '':
            self.pump.characteristic.delete_point(deleted_id)
        self.draw_figure()

    def print_values(self):
        objects = [self.well, self.pump, self.discharge_pipe, self.collector]
        for object_ in objects:
            log.debug(object_)
            for attr in object_.__dict__:
                log.debug(attr)
                if hasattr(object_.__dict__[attr], 'dan_id'):
                    log.debug('key: {}, val: {}'.format(
                        attr, object_.__dict__[attr]))

    def draw_figure(self, *args):
        log.debug('Starting draw_figure')
        self.plot.clear()
        self.canvas.draw()
        unit = self.ui_vars.__getitem__('pump_flow_unit').get()
        x = self.well.get_x_axis(unit)
        if self.pump.pump_char_ready():
            x, y_pump, l_pump = self.pump.draw_pump_plot(x)
            self.plot.plot(x, y_pump, l_pump, label='char. pompy')
        if self.well.pipes_ready():
            log.debug('Trying to drawing pipes plot')
            x, y_pipe, l_pipe = self.well.draw_pipes_plot(x, unit)
            log.debug('x: {}, y: {}, look: {}'.format(x, y_pipe, l_pipe))
            self.plot.plot(
                x, y_pipe, l_pipe, label='char. przewodów')
        if self.pump.pump_char_ready() and self.well.pipes_ready():
            try:
                intersection_f = maths.work_point(y_pump, y_pipe)
                self.plot.plot(x[intersection_f], y_pump[intersection_f], 'ro',
                               label='punkt pracy')
                str_work_p = str(round(x[intersection_f][0], 2))
            except IndexError as e:
                log.error('ERROR1: {}'.format(e))
                pass
        else:
            str_work_p = ''
        str_unit = classes.unit_bracket_dict[self.ui_vars.__getitem__(
            'pump_flow_unit').get()]
        self.plot.set_xlabel(
            'Przepływ Q {}'.format(str_unit))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        try:
            if len(x[intersection_f]) == 1:
                self.plot.set_title('Punkt pracy pompy: {} {}'.format(
                    str_work_p, str_unit))
            elif len(x[intersection_f]) > 1:
                list_points = [np.around(val, 2)
                               for val in x[intersection_f]]
                self.plot.set_title('Punkty pracy pompy: {} {}'.format(
                    list_points, str_unit))
        except UnboundLocalError:
            self.plot.set_title('Punkt pracy pompy: {} {}'.format(
                str_work_p, str_unit), fontsize='small')
            pass
        if unit == 'meters':
            self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        elif unit == 'liters':
            self.plot.xaxis.set_minor_locator(MultipleLocator(2))
        self.plot.yaxis.set_minor_locator(MultipleLocator(1))
        self.plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        self.plot.grid(True, 'major', linestyle='--')
        try:
            eff_from_x = self.pump.efficiency_from.value
            eff_from_y = maths.interp(eff_from_x, x, y_pump)
            eff_to_x = self.pump.efficiency_to.value
            eff_to_y = maths.interp(eff_to_x, x, y_pump)
            self.plot.plot([eff_from_x, eff_from_x], [-100, eff_from_y], 'r--')
            self.plot.plot([eff_to_x, eff_to_x], [-100, eff_to_y], 'r--',
                           label='maks. wydajność pompy')
            work_p_x = x[intersection_f]
            log.info('work_p_x: {}'.format(work_p_x))
            work_p_y = [maths.interp(i, x, y_pump) for i in work_p_x]
            for i in range(len(work_p_x)):
                self.plot.plot([work_p_x[i], work_p_x[i]],
                               [-100, work_p_y[i]], color='black',
                               linewidth=.8)
        except UnboundLocalError as e:
            log.error('Unbound ERROR2: {}'.format(e))
            pass
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=0)
        self.plot.legend(fontsize='small')
        self.canvas.draw()


if __name__ == '__main__':

    app = Application()
    app.run()
