# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk


class Application():
    """docstring for Application"""

    def __init__(self):

        self.station = station.Station()
        self.gui_tkinter = gui_tk.Gui()

    def run_gui(self):
        """ Makes infinite loop
        """
        self.gui_tkinter.mainwindow.mainloop()
