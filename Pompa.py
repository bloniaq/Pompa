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
    default = config.default

    def __init__(self):

        # 1: Create a builder
        self.builder = pygubu.Builder()

        # 2: Load an ui file
        self.builder.add_from_file('GUI_Pygubu.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = self.builder.get_object('Toplevel_Main')
        self.filepath = self.builder.get_object('filepath')
        self.pump_characteristic = {}

        # 4: Setting callbacks
        self.builder.connect_callbacks(self)

        # 5: creating objects

        self.create_objects()
        self.set_mode(self.default['mode'])

    def run(self):
        self.mainwindow.mainloop()

    def create_objects(self):
        self.well = classes.Well(self)
        self.bind_ui_variables(self.well, config.well_vars())
        self.set_inflow_unit()
        self.pump = classes.Pump(self)
        self.bind_ui_variables(self.pump, config.pump_vars())
        self.discharge_pipe = classes.Pipe(self)
        self.bind_ui_variables(
            self.discharge_pipe, config.discharge_pipe_vars())
        self.collector = classes.Pipe(self)
        self.bind_ui_variables(self.collector, config.collector_vars())

    def bind_ui_variables(self, instance, binder):
        setattr(instance, 'variables', binder)
        instance.bind_traceing_to_ui_variables()

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
        self.pump.load_data(data_dictionary)
        self.discharge_pipe.load_data(data_dictionary)
        self.collector.load_data(data_dictionary)

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
                    data_dictionary[id_] = int(data_dictionary[id_])
                    # expand for exceptions, make floats
                else:
                    data_dictionary[id_] = [float(s)
                                            for s in data_dictionary[id_]]
            log.debug('dictionary at finish: {}'.format(data_dictionary))
            return data_dictionary

    '''
    def dan_load(self, path):
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
                data_dictionary[id_line] = config.prepare_value(
                    id_line, data_dictionary[id_line])
                log.debug('dan_id: {0}) {1} <-readed_value'.format(
                    id_line, data_dictionary[id_line]))
        log.info(data_dictionary)
        log.info('dan load ended')
        log.info('load data started')
        self.builder.tkvariables.__getitem__('mode').set(data_dictionary['1'])
        self.ui_set_mode()
        self.builder.tkvariables.__getitem__('shape').set(data_dictionary['2'])
        self.ui_set_shape()
        self.well.load_data(data_dictionary)
        self.pump.load_data(data_dictionary)
        self.pump.load_characteristic_coords()
        self.discharge_pipe.load_data(data_dictionary)
        self.collector.load_data(data_dictionary)
    '''

    def ui_set_shape(self):
        shape = self.builder.tkvariables.__getitem__('shape').get()
        self.well.set_shape(shape)

    def ui_set_mode(self):
        mode = self.builder.tkvariables.__getitem__('mode').get()
        self.set_mode(mode)

    def set_mode(self, mode):
        ''' changes application mode
        '''
        self.builder.tkvariables.__getitem__('mode').set(mode)
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

    def set_var_value(self, variable_name, obj):
        log.info('app set_var_value starts for {}'.format(variable_name))
        log.info('variable_name type: {}'.format(type(variable_name)))
        value = self.builder.get_variable(variable_name).get()
        log.info('the value: {}'.format(value))
        obj.set_var_value(variable_name, value)

    def set_inflow_unit(self):
        log.info('changing unit of station inflow')
        unit = self.builder.tkvariables.__getitem__('inflow_unit').get()
        log.info('ui max value: {}'.format(
            self.builder.tkvariables.__getitem__('inflow_max').get()))
        log.info('engine max value: {}'.format(self.well.inflow_max.value))
        log.info('ooold value: {}'.format(self.builder.tkvariables.__getitem__(
            'inflow_min').get()))
        log.info('new unit: {}'.format(unit))
        self.well.inflow_max.convert(unit)
        self.well.inflow_min.convert(unit)
        self.builder.tkvariables.__getitem__('inflow_max').set(
            self.well.inflow_max.value)
        self.builder.tkvariables.__getitem__('inflow_min').set(
            self.well.inflow_min.value)

    def set_pump_flow_unit(self):
        log.info('set_pump_flow_unit started')
        current_setting = self.builder.tkvariables.__getitem__(
            'pump_flow_unit').get()
        self.pump.set_flow_unit(current_setting)

    def pump_get_coords(self):
        log.info('get_coords started')
        flow_entry = self.builder.get_object('Entry_Add_char_point_flow')
        flow_value = flow_entry.get()
        flow_entry.delete(0, 'end')
        lift_entry = self.builder.get_object('Entry_Add_char_point_lift')
        lift_value = lift_entry.get()
        lift_entry.delete(0, 'end')
        self.pump.add_point(flow_value, lift_value)

    def pump_delete_point(self):
        log.info('pump_delete_button started')
        deleted_id = self.pump.tree.focus()
        if deleted_id != '':
            self.pump.delete_point(deleted_id)

    def print_values(self):
        for key in self.well.variables:
            log.debug('{} - ui: {}, engine: {}'.format(
                key, self.builder.tkvariables.__getitem__(key).get(),
                getattr(self.well, self.well.variables[key][0])))
        for key in self.discharge_pipe.variables:
            try:
                log.debug('{} - ui: {}, engine: {}'.format(
                    key, self.builder.tkvariables.__getitem__(key).get(),
                    getattr(self.discharge_pipe,
                            self.discharge_pipe.variables[key][0])))
            except TypeError as e:
                log.error('TypeError: {}, attribute: {}, type: {}'.format(
                    e, self.discharge_pipe.variables[key][0], type(
                        self.discharge_pipe.variables[key][0])))
        for key in self.pump.variables:
            try:
                ui_item = self.builder.tkvariables.__getitem__(key).get()
            except KeyError as e:
                log.error('KeyError: {}, key: {} - not in builder'.format(
                    e, key))
            try:
                log.debug('{} - ui: {}, engine: {}'.format(
                    key, ui_item,
                    getattr(self.pump,
                            self.pump.variables[key][0])))
            except TypeError as e:
                log.error('TypeError: {}, attribute: {}, type: {}'.format(
                    e, self.pump.variables[key][0], type(
                        self.pump.variables[key][0])))

        log.debug('inflow engine value: {}'.format(self.well.inflow_max.value))
        log.debug('diam engine value: {}'.format(self.well.diameter))
        log.debug('res engine value: {}'.format(
            self.discharge_pipe.resistance.values))
        log.debug('types: diam: {}, res: {}'.format(
            type(self.well.diameter), type(
                self.discharge_pipe.resistance.values)))


if __name__ == '__main__':

    app = Application()
    app.run()
