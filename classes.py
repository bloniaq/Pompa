import logging

import config

log = logging.getLogger('Pompa/main.classes')


class Variable():

    def __init__(self, app):
        pass

    def set_var_value(self, variable_name, value):
        log.info('setting {} value to: {}'.format(variable_name, value))
        variable = self.builder.get_variable(variable_name)
        self.variables[variable_name][0] = value
        if variable.get() != value:
            variable.set(value)
        log.debug('{} - var value: {}, ui var value: {}'.format(
            variable_name, self.variables[variable_name][0], variable.get()))

    def bind_traceing_to_ui_variables(self, app):
        for variable in self.variables:
            variable_object = self.builder.get_variable(variable)
            variable_object.trace(
                'w', lambda *_, var=variable,
                obj=self: app.set_var_value(var, obj)
            )


class Flow():
    """class for flow"""

    def __init__(self, flow_val, flow_unit):
        self.value = flow_val
        self.unit = flow_unit

    def convert(self, new_unit):
        pass


class Lift():
    """class for lift"""

    def __init__(self, lift_val, lift_unit):
        self.value = lift_val
        self.unit = lift_unit

    def convert(self, new_unit):
        pass


class Pipe(Variable):
    """class for pipes"""

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.length = 0
        self.dimension = 0
        self.grittiness = 0
        self.local_resitance = []
        self.parallels = 1

    def resistance_to_cvar(self, variable):
        var = self.app.builder.get_variable(variable)


class Pump(Variable):
    """class for pumps"""

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.cycle_time = 0
        self.contour = 0
        self.characteristic = {}
        self.efficiency = []
        self.suction_level = 0

    def add_characteristic_points(
            self, point_id, flow_val, flow_unit, lift_val, lift_unit):
        flow = Flow(flow_val, flow_unit)
        lift = Lift(lift_val, lift_unit)
        self.characteristic[point_id] = (flow, lift)
        self.sort_characteristic_points()

    def sort_characteristic_points(self):
        pass


class Well(Variable):
    """class for well"""

    dan_shape = {'0': 'rectangle', '1': 'round'}
    dan_configuration = {'0': 'linear', '1': 'optimal'}
    dan_reserve = {'1': 'minimal', '2': 'optimal', '3': 'safe'}

    default = config.default

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.reserve_pumps = 'safe'
        self.shape = self.builder.tkvariables.__getitem__('shape')
        self.set_shape(self.default['shape'])
        self.diameter = 0
        self.length = 0
        self.width = 0
        self.ord_terrain = 0
        self.ord_inlet = 0
        self.ord_outlet = 0
        self.ord_bottom = 0
        self.ord_start = 0
        self.ord_highest_point = 0
        self.ord_upper_level = 0
        self.influx_max = 0
        self.influx_min = 0
        self.variables = {
            'well_diameter': [self.diameter],
            'well_length': [self.length],
            'well_width': [self.width]
        }
        self.bind_traceing_to_ui_variables(self.app)

    def set_shape(self, shape):
        self.builder.tkvariables.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = self.builder.get_object('Entry_Well_diameter')
        length = self.builder.get_object('Entry_Well_length')
        width = self.builder.get_object('Entry_Well_width')
        if shape == 'round':
            diameter.configure(state='normal')
            length.configure(state='disabled')
            width.configure(state='disabled')
        elif shape == 'rectangle':
            diameter.configure(state='disabled')
            length.configure(state='normal')
            width.configure(state='normal')
        log.debug('changed shape to {}'.format(shape))
