# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk


class Application:
    """Class used as the Contoller for instantiation the Application"""

    def __init__(self):

        self.station = station.Station()
        self.view_gui = gui_tk.Gui()

        self._add_callbacks()
        self._add_commands()

        self.view_gui.set_trace('well_diameter', self.gui_var_to_model)

    def run_gui(self):
        """Make infinite loop of GUI"""

        self.view_gui.mainwindow.mainloop()

    def gui_var_to_model(self, name_id):
        value = self.view_gui.ui_vars(name_id).get()
        if self.station.variables[name_id] != value:
            self.station.variables[name_id].set(value)

    def _add_callbacks(self):
        pass

    def _add_commands(self):
        self.view_gui.builder.get_object('Radio_Shape_round').config(
            command=self.set_shape_and_mode)
        self.view_gui.builder.get_object('Radio_Shape_rectangle').config(
            command=self.set_shape_and_mode)
        self.view_gui.builder.get_object('Radio_Mode_checking').config(
            command=self.set_shape_and_mode)
        self.view_gui.builder.get_object('Radio_Mode_minimalisation').config(
            command=self.set_shape_and_mode)

    def set_shape_and_mode(self):
        mode = self.view_gui.ui_vars.__getitem__('mode').get()
        shape = self.view_gui.ui_vars.__getitem__('shape').get()
        self.station.well.shape.set(shape)
        self.station.mode.set(mode)
        self.view_gui.ui_set_shape(shape, mode)
        self.view_gui.ui_set_mode(mode)
