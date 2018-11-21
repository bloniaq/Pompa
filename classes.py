import logging

import config

log = logging.getLogger('Pompa/main.classes')


class Variable():

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.variables = {}

    def __setattr__(self, attr, value):
        if '.' not in attr:
            self.__dict__[attr] = value
        else:
            attr_name, rest = attr.split('.', 1)
            setattr(getattr(self, attr_name), rest, value)

    def __getattr__(self, attr):
        if '.' not in attr:
            return self.__dict__[attr]
        else:
            attr_name, rest = attr.split('.', 1)
            return getattr(getattr(self, attr_name), rest)

    def set_var_value(self, variable_name, value):
        log.info('setting {} value to: {}'.format(variable_name, value))
        variable = self.builder.get_variable(variable_name)
        attribute = self.variables[variable_name][0]
        setattr(self, attribute, value)
        if variable.get() != value:
            variable.set(value)
        log.debug('{} - var value: {}, ui var value: {}'.format(
            variable_name, getattr(self, attribute), variable.get()))
        log.debug('diam engine value: {}'.format(self.diameter))

    def bind_traceing_to_ui_variables(self, app):
        for variable in self.variables:
            log.debug('variable: {}'.format(variable))
            variable_object = self.builder.get_variable(variable)
            variable_object.trace(
                'w', lambda *_, var=variable: app.set_var_value(var, self)
            )

    def set_flow_value(self, variable_name, value):
        pass


class Flow():
    """class for flow"""

    def __init__(self, flow_val, flow_unit):
        self.value = flow_val
        self.unit = flow_unit

    def convert(self, new_unit):
        log.info('conversion func starts')
        log.info('old value: {}'.format(self.value))
        if new_unit == self.unit:
            log.info('no need to conversion')
            return
        elif new_unit == 'meters':
            self.unit = new_unit
            self.value *= 3.6
        elif new_unit == 'liters':
            self.unit = new_unit
            self.value /= 3.6
        log.info('new value: {}'.format(self.value))


class Resistance():
    """class for lift"""

    def __init__(self):
        self.string = ''
        self.values = []

    def __setattr__(self, attribute, value):
        if attribute != 'string':
            super().__setattr__(attribute, value)
        elif value != '':
            super().__setattr__(attribute, value)
            self.values = [float(s) for s in value.split(',')]


class Pipe(Variable):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = Resistance()
        self.parallels = 1


'''
    def resistance_to_cvar(self, variable):
        var = self.app.builder.get_variable(variable)
'''


class Pump(Variable):
    """class for pumps"""

    def __init__(self, app):
        super().__init__(app)
        self.cycle_time = 0
        self.contour = 0
        self.characteristic = {}
        self.efficiency = []
        self.suction_level = 0

    def add_characteristic_points(
            self, point_id, flow_val, flow_unit, lift_val, lift_unit):
        flow = Flow(flow_val, flow_unit)
        self.characteristic[point_id] = (flow)
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
        super().__init__(app)
        self.reserve_pumps = 'safe'
        self.shape = self.builder.tkvariables.__getitem__('shape')
        self.set_shape(self.default['shape'])
        self.diameter = 0
        self.length = 0
        self.width = 0
        self.minimal_sewage_level = 0
        self.ord_terrain = 0
        self.ord_inlet = 0
        self.ord_outlet = 0
        self.ord_bottom = 0
        self.difference_in_start = 0
        self.ord_highest_point = 0
        self.ord_upper_level = 0
        self.inflow_max = Flow(0, 'liters')
        self.inflow_min = Flow(0, 'liters')
        # self.bind_traces_manual(self.app)

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

    def bind_traces_manual(self, app):
        variable = 'inflow_max'
        log.debug('variable: {}'.format(variable))
        variable_object = self.builder.get_variable(variable)
        variable_object.trace(
            'w', lambda *_,
            var=variable: app.set_var_value(var, self.inflow_max)
        )
