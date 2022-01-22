# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk

# TEST PURPOSES ONLY (VIEW BUILD)
import numpy as np


DEVELOPER_MODE = True


class Application:
    """Class used as the Controller for instantiation the Application"""

    STRING_VARIABLES = (
        'mode',
        'shape',
        'config',
        'safety',
        'unit'
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
        'mode': 'checking',
        'shape': 'round',
        'config': 'singlerow',
        'safety': 'optimal',
        'unit': 'meters'
    }

    def __init__(self):

        self.model = station.Station()
        self.view = gui_tk.View(self.VARIABLES, self.DEFAULT_VALUES)

        if DEVELOPER_MODE:
            # TESTING FIGURES CREATING ONLY
            self.draw_possible_figures()

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

    # DRAWING FIGURES

    def draw_possible_figures(self):
        """
        WARNING!
        It does not do it's future job right now - while View is still not
        finished. Although it plays a role as testing Mock-like initiator of
        figures. That should be its only purpose until the view is completed.
        Then the method should be recoded from scratch
        """
        # 0. Arranging environment
        mock_pipe = self.model.ins_pipe
        mock_hc = self.model.hydr_cond
        mock_hc.inflow_min.set(1, 'm3ps')
        mock_hc.inflow_max.set(2, 'm3ps')
        mock_pipe.length.set(8)
        mock_pipe.diameter.set(.250)
        mock_pipe.roughness.set(.00001)

        # 1. Ask model which figures are ready to draw
        availability = {
            'ins_pipe': True
        }

        # 2. Get available data from model
        flows_array = np.linspace(
            mock_hc.inflow_min.value_m3ps,
            1.4 * mock_hc.inflow_max.value_m3ps,
            200
        )
        print(f"min inflow: {mock_hc.inflow_min}")
        print(f"max inflow: {mock_hc.inflow_max}")
        ins_pipe_poly_coeffs = mock_pipe.dynamic_loss_polynomial(
            mock_hc.inflow_min,
            mock_hc.inflow_max
        )

        args = {
            'x': flows_array,
            'ins_pipe': np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs)
        }

        # 3. Draw possible figures
        for figure in availability.keys():
            if availability[figure]:
                self.view.draw_figure(figure)(
                    args['x'],
                    args[figure]
                )
