# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk

# TEST PURPOSES ONLY (VIEW BUILD)
import numpy as np


DEVELOPER_MODE = True


class VMVar:
    """ViewModel Variable"""

    controller = None

    def __init__(self, name, type, default_value):
        self.name = name
        self.type = type
        self.default_value = default_value
        self.viewvar = None
        self.modelvar = None

    def set_viewvar_callback(self):
        self.viewvar.trace_add(self.set_in_model)

    def set_in_model(self):
        self._modelvar().set(self.viewvar.get())

    def _modelvar(self):
        return self.controller.model.get_var(self.name)


class Application:
    """Class used as the ViewModel for instantiation the Application"""

    # Arguments for VMVar class constructor:
    # (name, type, default_value)
    _variables_init_values = [
        ('mode', 'string', 'checking'),
        ('shape', 'string', 'round'),
        ('config', 'string', 'singlerow'),
        ('safety', 'string', 'optimal'),
        ('unit', 'string', 'meters'),
        ('parallel_out_pipes', 'int', 1),
        ('ord_terrain', 'double', None)
    ]

    def __init__(self):

        # Initializing Application (ViewModel) variables
        VMVar.controller = self
        self.variables = self._init_variables()

        # Creating View and Model
        self.model = station.Station()
        self.view = gui_tk.View(self.variables)

        # Variables binding

        if DEVELOPER_MODE:
            # TESTING FIGURES CREATING ONLY
            self.draw_possible_figures()

        # self._add_callbacks()
        # self._add_commands()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.view.quit()
        del self

    def run_gui(self):
        """Make infinite loop of GUI"""

        self.view.run()

    def _add_callbacks(self):
        pass

    @classmethod
    def _init_variables(cls):
        """
        init_values: tuple with all necessary data for binding and creating variables both in model and in view
        """
        variables = []
        for variable_params in cls._variables_init_values:
            variable = VMVar(*variable_params)
            variables.append(variable)

        return variables

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
        mock_pump = self.model.pump_type
        mock_hc.inflow_min.set(10, 'm3ph')
        mock_hc.inflow_max.set(20, 'm3ph')
        mock_hc.ord_terrain.set(100)
        mock_hc.ord_highest_point.set(110)
        mock_hc.ord_upper_level.set(110)
        mock_pipe.length.set(8)
        mock_pipe.diameter.set(.250)
        mock_pipe.roughness.set(.00001)

        # 1. Ask model which figures are ready to draw
        availability = {
            'ins_pipe': True,
            'geometric_height': True
        }

        # 2. Get available data from model
        flows_array = np.linspace(
            mock_hc.inflow_min.value_m3ps,
            1.4 * mock_hc.inflow_max.value_m3ps,
            5
        )
        ins_pipe_poly_coeffs = mock_pipe.dynamic_loss_polynomial(
            mock_hc.inflow_min,
            mock_hc.inflow_max
        )

        args = {
            'x': flows_array,
            'ins_pipe': np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs) + mock_hc.geom_height(mock_hc.ord_terrain).get(),
            'geometric_height': np.polynomial.polynomial.Polynomial(
                [mock_hc.geom_height(mock_hc.ord_terrain).get()]
            )
        }

        # 3. Draw possible figures
        for figure in availability.keys():
            if availability[figure]:
                self.view.draw_figure(figure)(
                    args['x'],
                    args[figure],
                    'meters'
                )
