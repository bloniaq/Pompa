# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk


class Application:
    """Class used as the Contoller for instantiation the Application"""

    def __init__(self):

        self.station = station.Station()
        self.view_gui = gui_tk.Gui()

    def run_gui(self):
        """Make infinite loop of GUI"""

        self.view_gui.mainwindow.mainloop()

    def add_callback(self):
        pass

    def set_shape(self, shape):
        mode = self.view_gui.ui_vars.__getitem__('mode')
        self.view_gui.set_shape(shape, mode)
