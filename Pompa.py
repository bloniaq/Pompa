import tkinter as tk  # for python 3
'''
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
'''
import pygubu
import logging

import classes
import config
import data

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

variables_list = []
path = ""

# LOGGING CONFIGURATION

# clearing root logger handlers
log = logging.getLogger()
log.handlers = []

# setting new logger
log = logging.getLogger('Pompa/main')
log.setLevel(logging.DEBUG)

# create console and file handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('logfile.log', 'w')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s',
                              datefmt='%Y.%m.%d %H:%M:%S')

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

        self.figure = fig = Figure(figsize=(4, 5.1), dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=fcontainer)
        canvas.get_tk_widget().grid(row=0, column=0)

        # 4: Setting callbacks
        self.builder.connect_callbacks(self)

        # 5: creating objects

        self.create_objects()
        self.set_mode(self.default['mode'])

    def on_plot_clicked(self):
        a = self.figure.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        self.canvas.draw()

    def run(self):
        self.mainwindow.mainloop()

    def create_objects(self):
        self.well = classes.Well(self)
        data.well_vars(self.well, self)
        self.pump = classes.Pump(self)
        data.pump_vars(self.pump, self, self.figure, self.canvas)
        self.pump.set_flow_unit(
            self.ui_vars.__getitem__('pump_flow_unit').get())
        self.discharge_pipe = classes.Pipe(self)
        data.discharge_pipe_vars(self.discharge_pipe, self)
        self.collector = classes.Pipe(self)
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

    def pump_delete_point(self):
        log.info('pump_delete_button started')
        deleted_id = self.pump.characteristic.tree.focus()
        if deleted_id != '':
            self.pump.characteristic.delete_point(deleted_id)

    def print_values(self):
        objects = [self.well, self.pump, self.discharge_pipe, self.collector]
        for object_ in objects:
            log.debug(object_)
            for attr in object_.__dict__:
                log.debug(attr)
                if hasattr(object_.__dict__[attr], 'dan_id'):
                    log.debug('key: {}, val: {}'.format(
                        attr, object_.__dict__[attr]))


if __name__ == '__main__':

    app = Application()
    app.run()
