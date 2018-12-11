import tkinter as tk  # for python 3
import pygubu
import logging
import numpy as np

import components
import station
import maths
import data
import output

from matplotlib.ticker import MultipleLocator

variables_list = []
path = ""

# LOGGING CONFIGURATION

log = logging.getLogger()
log.handlers = []

log = logging.getLogger('Pompa')
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


class Application():

    dan_mode = {'0': 'minimalisation', '1': 'checking', '2': 'optimalisation'}
    default = data.default

    def __init__(self):

        # 1: Create a builder
        self.builder = pygubu.Builder()

        # 2: Load an ui file
        self.builder.add_from_file('GUI_Pygubu_Rebuild.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = self.builder.get_object('Toplevel_Main')
        self.filepath = self.builder.get_object('filepath')
        self.ui_vars = self.builder.tkvariables

        # 4: Setting callbacks
        self.builder.connect_callbacks(self)

        # 5: creating objects
        self.init_objects()
        self.set_mode(self.default['mode'])

        # 6: Initialize Figure objects
        pump_figure_cont = self.builder.get_object('Frame_Pump_Figure')
        pipe_figure_cont = self.builder.get_object('Frame_Pipe_Figure')
        station_figure_cont = self.builder.get_object('Frame_Station_Figure')
        report_figure_cont = self.builder.get_object('Frame_Report_Figure')
        self.pump_figure, self.pump_plot, self.pump_canvas = maths.init_figure(
            pump_figure_cont, 4.2, 5.1)
        self.pipe_figure, self.pipe_plot, self.pipe_canvas = maths.init_figure(
            pipe_figure_cont, 4.2, 5.1)
        self.stat_figure, self.stat_plot, self.stat_canvas = maths.init_figure(
            station_figure_cont, 4.2, 5.1)
        self.rep_figure, self.rep_plot, self.rep_canvas = maths.init_figure(
            report_figure_cont, 4.2, 5.1)
        self.pump_canvas.get_tk_widget().grid(row=0, column=0)
        self.pipe_canvas.get_tk_widget().grid(row=0, column=0)
        self.stat_canvas.get_tk_widget().grid(row=0, column=0)
        self.rep_canvas.get_tk_widget().grid(row=0, column=0)

    def init_objects(self):
        self.station = station.Station(self)
        data.station_vars(self)
        self.well = self.station.well = components.Well(self)
        data.well_vars(self)
        self.pump_type = self.station.pump_type = components.PumpType(self)
        data.pump_vars(self)
        self.pump_type.set_flow_unit(
            self.ui_vars.__getitem__('pump_flow_unit').get())
        self.d_pipe = self.station.d_pipe = components.Pipe(self)
        data.discharge_pipe_vars(self)
        self.collector = self.station.collector = components.Pipe(self)
        data.collector_vars(self)

    def run(self):
        self.mainwindow.mainloop()

    def calculate(self):
        if self.mode == 'checking':
            self.station.calculate()
            out_data = output.generate_checking_report(self.well)
        self.generate_report(out_data)

    def generate_report(self, output):
        pass

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
                data_dictionary = data.get_data_dict_from_dan_file(path)
        self.station.load_data(data_dictionary)
        self.well.load_data(data_dictionary)
        self.d_pipe.load_data(data_dictionary)
        self.collector.load_data(data_dictionary)
        self.pump_type.load_data(data_dictionary)
        self.draw_report_figure()

    def ui_set_shape(self):
        shape = self.ui_vars.__getitem__('shape').get()
        self.well.set_shape(shape)

    def ui_set_mode(self):
        self.mode = self.ui_vars.__getitem__('mode').get()
        self.set_mode(self.mode)

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
        self.pump_type.set_flow_unit(current_setting)
        log.debug('going to draw figure')
        self.draw_report_figure()

    def pump_get_coords(self):
        log.info('get_coords started')
        flow_entry = self.builder.get_object('Entry_Add_char_point_flow')
        flow_value = flow_entry.get()
        flow_entry.delete(0, 'end')
        lift_entry = self.builder.get_object('Entry_Add_char_point_lift')
        lift_value = lift_entry.get()
        lift_entry.delete(0, 'end')
        self.pump_type.characteristic.add_point(flow_value, lift_value)
        self.pump_type.characteristic.sort_points()
        self.draw_report_figure()

    def pump_delete_point(self):
        log.info('pump_delete_button started')
        deleted_id = self.pump_type.characteristic.tree.focus()
        if deleted_id != '':
            self.pump_type.characteristic.delete_point(deleted_id)
        self.draw_report_figure()

    def print_values(self):
        objects = [self.well, self.pump_type, self.d_pipe, self.collector]
        for object_ in objects:
            log.debug(object_)
            for attr in object_.__dict__:
                log.debug(attr)
                if hasattr(object_.__dict__[attr], 'dan_id'):
                    log.debug('key: {}, val: {}'.format(
                        attr, object_.__dict__[attr]))

    def draw_report_figure(self):
        maths.draw_report_figure(self.builder, self.rep_plot, self.rep_canvas,
                                 self.station)


if __name__ == '__main__':

    app = Application()
    app.run()
