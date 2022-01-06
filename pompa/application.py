# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk


class Application:
    """Class used as the Contoller for instantiation the Application"""

    STRING_VARIABLES = (
        'unit',
        'mode',
        'safety',
        'shape'
    )
    INT_VARIABLES = (
        'parallel_out_pipes'
    )
    DOUBLE_VARIABLES = (
        'ord_terrain'
    )
    VARIABLES = {
        'string_ids': STRING_VARIABLES,
        'int_ids': INT_VARIABLES,
        'double_ids': DOUBLE_VARIABLES
    }
    DEFAULT_VALUES = {
        'unit': 'meters',
        'mode': 'checking',
        'safety': 'optimal',
        'shape': 'round'
    }

    def __init__(self):

        self.station = station.Station()
        self.view = gui_tk.View(self.VARIABLES, self.DEFAULT_VALUES)

        # self._add_callbacks()
        # self._add_commands()

    def run_gui(self):
        """Make infinite loop of GUI"""

        self.view.run()

    def _add_callbacks(self):
        pass

    """
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
        self.view_gui.ui_set_shape(shape, mode)
        self.view_gui.ui_set_mode(mode)"""
