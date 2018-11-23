try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
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
        self.tree = self.builder.get_object('Treeview_Pump')
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
        self.bind_ui_variables(self.well, config.well_vars(self.well))
        self.set_inflow_unit()
        self.pump = classes.Pump(self)
        # self.bind_ui_variables(self.pump)
        self.discharge_pipe = classes.Pipe(self)
        self.bind_ui_variables(
            self.discharge_pipe, config.discharge_pipe_vars(self.well))
        self.collector = classes.Pipe(self)
        # self.bind_ui_variables(self.collector)

    def bind_ui_variables(self, instance, binder):
        setattr(instance, 'variables', binder)
        instance.bind_traceing_to_ui_variables(self)

    def load_data(self):
        pass

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
        pass

    def pump_get_coords(self):
        log.info('get_coords started')
        entry_q = self.builder.get_object('Entry_Add_char_point_flow')
        val_q = entry_q.get()
        entry_q.delete(0, 'end')
        entry_h = self.builder.get_object('Entry_Add_char_point_lift')
        val_h = entry_h.get()
        entry_h.delete(0, 'end')
        # self.pump_add_point(val_q, val_h)

    def print_values(self):
        for key in self.well.variables:
            log.debug('{} - ui: {}, engine: {}'.format(
                key, self.builder.tkvariables.__getitem__(key).get(),
                getattr(self.well, self.well.variables[key][0])))
        log.debug('inflow engine value: {}'.format(self.well.inflow_max.value))
        log.debug('diam engine value: {}'.format(self.well.diameter))
        log.debug('res engine value: {}'.format(
            self.discharge_pipe.resistance.values))


if __name__ == '__main__':

    app = Application()
    app.run()
