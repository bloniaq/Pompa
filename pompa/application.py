# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk

# TEST PURPOSES ONLY (VIEW BUILD)
import numpy as np


DEVELOPER_MODE = True


class VMVar:
    """ViewModel Variable"""

    controller = None

    def __init__(self, name: str, id_: int, type_: str, default_value):
        self.name = name
        self.id = id_
        self.type = type_
        self.default_value = default_value
        self.viewvar = None
        self.gui_widget = None
        self.modelvar = None

    def set_in_model(self, value):
        if self.type == 'flow':
            unit = self.viewvar.get_current_unit()
            self.modelvar.set(value, unit)
            print(f"{self.name} is seting {value} to model: {self.modelvar.get_by_unit(unit)} {unit}")
        elif self.type == 'res':
            resistances_string = list(value.split(";"))
            resistances_float = [float(res) for res in resistances_string]
            self.modelvar.set(resistances_float)
            print(f"{self.name} is seting {value} to model: {self.modelvar.get()}")
        elif self.type == 'pump_char':
            self.modelvar.value.clear()
            for point in value:
                self.modelvar.add_point(
                    point['flow'], point['height'], point['unit'])
            print(f"{self.name} is setting {value} to model: {self.modelvar.value}")
        else:
            self.modelvar.set(value)
            print(f"{self.name} is seting {value} to model: {self.modelvar.get()}")

    def return_value_for_unit(self, unit):
        return self.modelvar.get_by_unit(unit)

class Application:
    """Class used as the ViewModel  for instantiation the Application"""

    # Arguments for VMVar class constructor:
    # (name, type, default_value)
    _variables_init_values = [
        ('mode', 1, 'string', 'checking'),
        ('shape', 2, 'string', 'round'),
        ('config', 3, 'string', 'singlerow'),
        ('safety', 4, 'string', 'optimal'),
        ('pump_contour', 5, 'double', None),
        ('well_length', 6, 'double', None),
        ('well_width', 7, 'double', None),
        ('well_diameter', 8, 'double', None),
        ('suction_level', 9, 'double', None),
        ('ord_terrain', 10, 'double', None),
        ('ord_outlet', 11, 'double', None),
        ('ord_inlet', 12, 'double', None),
        ('ord_bottom', 13, 'double', None),
        ('reserve_height', 14, 'double', None),
        ('ord_highest_point', 15, 'double', None),
        ('ord_upper_level', 16, 'double', None),
        # TODO: Sprawdzić te id poniżej
        ('ins_pipe_length', 28, 'double', None),
        ('ins_pipe_diameter', 29, 'double', None),
        ('ins_pipe_roughness', 30, 'double', None),
        ('ins_pipe_resistances', 32, 'res', None),
        ('inflow_min', 33, 'flow', None),
        ('inflow_max', 34, 'flow', None),
        ('min_cycle_time', 35, 'double', None),
        ('pump_characteristic', 37, 'pump_char', None),
        ('pump_eff_min', 39, 'flow', None),
        ('pump_eff_max', 40, 'flow', None),
        ('parallel_out_pipes', 41, 'int', 1),
        ('out_pipe_length', 42, 'double', None),
        ('out_pipe_diameter', 43, 'double', None),
        ('out_pipe_roughness', 44, 'double', None),
        ('out_pipe_resistances', 46, 'res', None),
        ('unit', 100, 'string', 'm3ph')
    ]

    def __init__(self):

        # Initializing Application (ViewModel) variables
        VMVar.controller = self
        self.variables = self._init_variables()

        # Creating View and Model
        self.model = station.Station()
        self.model.bind_variables(self.variables)
        # binding model vars from here, instead of passing variables to init
        # to provide testability of model
        self.view = gui_tk.View(self.variables)

        # # Variables binding
        # for var in self.variables:
        #     var.set_viewvar_callback()

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
                ins_pipe_poly_coeffs) + mock_hc.geom_height(mock_hc.ord_terrain),
            'geometric_height': np.polynomial.polynomial.Polynomial(
                [mock_hc.geom_height(mock_hc.ord_terrain)]
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
