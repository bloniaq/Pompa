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

        self.clear_objects()
        self.set_mode(default=True)
        self.load_last_data()

    def run(self):
        self.mainwindow.mainloop()

    def clear_objects(self):
        self.well = classes.Well(self.builder)
        self.pump = classes.Pump(self.builder)
        self.inlet = classes.Pipe(self.builder)
        self.outlet = classes.Pipe(self.builder)

    def load_last_data(self):
        pass

    def ui_set_shape(self):
        shape = self.builder.tkvariables.__getitem__('shape').get()
        self.well.set_shape(shape)

    def set_mode(self, default=False):
        ''' changes application mode
        '''
        self.dan_mode = {'0': 'minimalisation',
                         '1': 'checking', '2': 'optimalisation'}
        item = self.builder.tkvariables.__getitem__('mode')
        mode = item.get()
        if default:
            mode = 'checking'
            item.set(mode)
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


if __name__ == '__main__':

    app = Application()
    app.run()
