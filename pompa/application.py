# -*- coding: utf-8 -*-

import pompa.models.station as station
import pompa.view.gui_tk as gui_tk
from collections import namedtuple
from pompa.exceptions import BrokenDataError

# TEST PURPOSES ONLY (VIEW BUILD)
import numpy as np

class VMVar:
    """ViewModel Variable"""

    controller = None

    def __init__(self, name: str, id_: int, default_value):
        self.name = name
        self.id = id_
        self.type = "type"
        self.default_value = default_value
        self.viewvar = None
        self.gui_widget = None
        self.modelvar = None

    def set_in_model(self, value):
        self.modelvar.set(value)
        print(f"{self.name} is seting {value} to model: {self.modelvar.get()}")

    def set_in_view(self, value):
        self.viewvar.set(value)
        print(f"{self.name} is seting {value} to view: {self.viewvar.get()}")

    def return_value_for_unit(self, unit):
        return self.modelvar.get_by_unit(unit)


class StringVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value, dictionary=None):
        super().__init__(name, id_, default_value)
        self.type = "string"
        self.dictionary = dictionary

    def load_data(self, data, *args):
        if self.dictionary is not None:
            value = self.dictionary[data[self.id][0]]
        else:
            value = data[self.id][0]
        self.set_in_model(value)
        self.set_in_view(value)


class DoubleVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value, multipl=1):
        # multiplayer added for cover differences between the units in view and
        # in model, specifically in pipe diameter parameter
        # it equals view_unit/model_unit
        # if there's i.e. meters in model, and milimeters in view, multipl=.001
        super().__init__(name, id_, default_value)
        self.multipl = multipl
        self.type = "double"

    def load_data(self, data, *args):
        value = float(data[self.id][0])
        self.set_in_view(value)
        self.set_in_model(value)

    def set_in_model(self, value):
        # multiplayer added for cover differences between the units in view and
        # in model, specifically in pipe diameter parameter
        self.modelvar.set(value * self.multipl)
        print(f"{self.name} is seting {value} to model: {self.modelvar.get()}")


class IntVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value):
        super().__init__(name, id_, default_value)
        self.type = "int"

    def load_data(self, data, *args):
        value = int(data[self.id][0])
        self.set_in_view(value)
        self.set_in_model(value)


class ResVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value):
        super().__init__(name, id_, default_value)
        self.type = "res"

    def load_data(self, data, *args):
        res_list = data[self.id]
        res_list = map(float, res_list)
        res_list = map(str, res_list)
        string_format = '; '.join(res_list)
        self.set_in_view(string_format)
        self.set_in_model(string_format)


    def set_in_model(self, value):
        resistances_string = list(value.split(";"))
        if resistances_string == ['']:
            resistances_string = ['0']
        resistances_float = [float(res) for res in resistances_string]
        self.modelvar.set(resistances_float)
        print(f"{self.name} is seting {value} to model: {self.modelvar.get()}")


class FlowVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value):
        super().__init__(name, id_, default_value)
        self.type = "flow"

    def load_data(self, data, unit):
        value = float(data[self.id][0])
        self.set_in_model(value, 'lps')
        self.set_in_view(self.modelvar.get_by_unit('lps'))

    def set_in_model(self, value, unit=None):
        if unit is None:
            unit = self.viewvar.get_current_unit()
        self.modelvar.set(value, unit)
        print(f"{self.name} is seting {value} to model: {self.modelvar.get_by_unit(unit)} {unit}")


class PumpCharVMVar(VMVar):

    def __init__(self, name: str, id_: int, default_value):
        super().__init__(name, id_, default_value)
        self.type = "pump_char"

    def load_data(self, data, unit):
        flow_list = data[self.id]
        height_list = data[self.id + 1]
        if not len(flow_list) == len(height_list):
            raise BrokenDataError
        else:
            self.viewvar.clear_points()
            for coord in range(len(flow_list)):
                self.viewvar.add_point(unit,
                                       flow_list[coord],
                                       height_list[coord])

    def set_in_model(self, value):
        self.modelvar.value.clear()
        for point in value:
            self.modelvar.add_point(
                point['flow'], point['height'], point['unit'])
        print(f"{self.name} is setting {value} to model: {self.modelvar.value}")


class Application:
    """Class used as the ViewModel  for instantiation the Application"""

    # Arguments for VMVar class constructor:
    # (name, type, default_value)
    _variables_init_values = [
        ('mode', 1, 'string', 'checking', {"0": "minimalisation", "1": "checking"}),
        ('shape', 2, 'string', 'round', {"0": "rectangle", "1": "round"}),
        ('config', 3, 'string', 'singlerow', {"0": "singlerow", "1": "optimal"}),
        ('safety', 4, 'string', 'optimal', {"1": "economic", "2": "optimal", "3": "safe"}),
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
        ('ins_pipe_diameter', 29, 'double', None, 0.001),
        ('ins_pipe_roughness', 30, 'double', None, 0.001),
        ('ins_pipe_resistances', 32, 'res', None),
        ('inflow_min', 33, 'flow', None),
        ('inflow_max', 34, 'flow', None),
        ('min_cycle_time', 35, 'double', None),
        ('pump_characteristic', 37, 'pump_char', None),
        ('pump_eff_min', 39, 'flow', None),
        ('pump_eff_max', 40, 'flow', None),
        ('parallel_out_pipes', 41, 'int', 1),
        ('out_pipe_length', 42, 'double', None),
        ('out_pipe_diameter', 43, 'double', None, 0.001),
        ('out_pipe_roughness', 44, 'double', None, 0.001),
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
        self.view.loadfile_procedure = self.load_file
        self.view.savefile_procedure = self.save_file
        self.view.get_results_procedure = self.get_results
        self.view.draw_figures_procedure = self.draw_possible_figures

        # # Variables binding
        # for var in self.variables:
        #     var.set_viewvar_callback()

        self.view.draw_figures_procedure()

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
        variables = {}
        var_type = {
            "string": StringVMVar,
            "double": DoubleVMVar,
            "int": IntVMVar,
            "res": ResVMVar,
            "flow": FlowVMVar,
            "pump_char": PumpCharVMVar
        }
        # Changing data format to realize subclassing VMVar
        init_data = []
        Record = namedtuple('Record', ['type', 'data'])
        for v_tuple in cls._variables_init_values:
            v_list = list(v_tuple)
            type_ = v_list.pop(2)
            data = tuple(v_list)
            init_data.append(Record(type_, data))
        #
        for var_params in init_data:
            variable = var_type[var_params.type](*var_params.data)
            variables[variable.name] = variable

        return variables

    # DRAWING FIGURES

    def draw_possible_figures(self):

        data = self.model.get_figure_data()
        result = self.view.update_figures(
            data['pipechart_data'],
            data['pumpchart_data']
        )
        print(result)

    def get_var_by_name(self, name):
        for v in self.variables.values():
            if v.name == name:
                return v

    def get_var_by_id(self, id_):
        for v in self.variables.values():
            if v.id == id_:
                return v

    def load_file(self, file, unit):
        data = self.read_file(file)
        for v in self.variables.values():
            if v.id in data.keys():
                v.load_data(data, unit)

        return data

    def read_file(self, file):
        data = {}
        with open(file, 'r') as f:
            file_data = f.read()
        for line in file_data.split('\n'):
            if ')' not in line:
                continue
            [key, value] = line.split(')')
            if int(key) in data.keys():
                data[int(key)].append(value.strip())
            else:
                data[int(key)] = [value.strip()]
        print(data)
        return data

    def save_file(self, file):
        v = self.variables

        def get_symbol_for_string_var(name):
            for key, val in v[name].dictionary.items():
                if val == v[name].modelvar.value:
                    return key

        with open(file + ".DAN", 'w') as f:
            f.write(f"1){get_symbol_for_string_var('mode')}\n")
            f.write(f"2) {get_symbol_for_string_var('shape')}\n")
            f.write(f"3) {get_symbol_for_string_var('config')}\n")
            f.write(f"4){get_symbol_for_string_var('safety')}\n")
            f.write(f"5) {v['pump_contour'].modelvar.value}\n")
            if self.model.well.shape.get() == 'rectangle':
                f.write(f"6) {v['well_length'].modelvar.value}\n")
                f.write(f"7) {v['well_width'].modelvar.value}\n")
            elif self.model.well.shape.get() == 'rectangle':
                f.write(f"8) {v['well_diameter'].modelvar.value}\n")
            f.write(f"9) {v['suction_level'].modelvar.value}\n")
            f.write(f"10) {v['ord_terrain'].modelvar.value}\n")
            f.write(f"11) {v['ord_outlet'].modelvar.value}\n")
            f.write(f"12) {v['ord_inlet'].modelvar.value}\n")
            f.write(f"13) {v['ord_bottom'].modelvar.value}\n")
            if self.model.mode.get() == 'minimalisation':
                f.write(f"14) {v['reserve_height'].modelvar.value}\n")
            f.write(f"15) {v['ord_highest_point'].modelvar.value}\n")
            f.write(f"16) {v['ord_upper_level'].modelvar.value}\n")
            f.write(f"28) {v['ins_pipe_length'].modelvar.value}\n")
            f.write(f"29) {v['ins_pipe_diameter'].modelvar.value * 1000}\n")
            f.write(f"30) {v['ins_pipe_roughness'].modelvar.value * 1000}\n")
            ins_pipe_res_count = len(v['ins_pipe_resistances'].modelvar.value)
            f.write(f"31) {ins_pipe_res_count}\n")
            if ins_pipe_res_count > 0:
                for res in v['ins_pipe_resistances'].modelvar.value:
                    f.write(f"32) {res}\n")
            f.write(f"33) {v['inflow_min'].modelvar.value_lps}\n")
            f.write(f"34) {v['inflow_max'].modelvar.value_lps}\n")
            f.write(f"35) {round(v['min_cycle_time'].modelvar.value, 1)}\n")
            pump_char_points_count = len(v['pump_characteristic'].modelvar.value)
            f.write(f"36){pump_char_points_count}\n")
            if pump_char_points_count > 0:
                points_list = list(reversed(v['pump_characteristic'].modelvar.value))
                for point in points_list:
                    f.write(f"37) {point[0].value_lps}\n")
                for point in points_list:
                    f.write(f"38) {point[1]}\n")
            f.write(f"39) {v['pump_eff_min'].modelvar.value_lps}\n")
            f.write(f"40) {v['pump_eff_max'].modelvar.value_lps}\n")
            f.write(f"41) {int(v['parallel_out_pipes'].modelvar.value)}\n")
            f.write(f"42) {v['out_pipe_length'].modelvar.value}\n")
            f.write(f"43) {v['out_pipe_diameter'].modelvar.value * 1000}\n")
            f.write(f"44) {v['out_pipe_roughness'].modelvar.value * 1000}\n")
            out_pipe_res_count = len(v['out_pipe_resistances'].modelvar.value)
            f.write(f"45) {out_pipe_res_count}\n")
            if out_pipe_res_count > 0:
                for res in v['out_pipe_resistances'].modelvar.value:
                    f.write(f"46) {res}\n")

    def get_results(self):
        self.model.calculate(self.model.mode.value)
        results = self.model.pumpsystem
        station = self.model
        return results, station
