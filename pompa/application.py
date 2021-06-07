# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk


class Application:
    """Class used for instantiation the Application"""

    def __init__(self):

        self.station = station.Station()
        self.gui_tkinter = gui_tk.Gui()

    def run_gui(self):
        """Make infinite loop of GUI"""

        self.gui_tkinter.mainwindow.mainloop()
