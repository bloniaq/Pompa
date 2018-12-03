import logging

import maths

log = logging.getLogger('Pompa.classes')
unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


class StationObject():

    kinematic_viscosity = 1.0068  # [mm²/s] dla 20°C
    std_grav = 9.81

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.ui_vars = app.builder.tkvariables

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

    def load_data(self, data_dict):
        for attribute in self.__dict__:
            if hasattr(self.__dict__[attribute], 'dan_id'):
                self.__dict__[attribute].load_data(data_dict)


class Pipe(StationObject):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = 0
        self.parallels = 1

    def get_re(self, flow, unit):
        diameter = self.diameter.value
        speed = 1000 * self.speed(flow, unit)
        re = (diameter * speed) / self.kinematic_viscosity
        log.info('Reynolds number is {}'.format(re))
        return re

    def get_epsilon(self):
        diameter = self.diameter.value
        epsilon = self.roughness.value / diameter
        return epsilon

    def get_lambda(self, flow, unit):
        diameter = self.diameter.value * 0.001
        epsilon = self.get_epsilon()
        log.info('Epsilon is {}'.format(epsilon))
        lambda_ = (-2 * maths.log10(self.roughness.value / (
            3.71 * diameter))) ** -2
        re = self.get_re(flow, unit)
        log.info('Re is {}'.format(re))
        log.info('Lambda is {}'.format(lambda_))
        try:
            alt_lambda = (-2 * maths.log10((6.1 / (re ** 0.915)) + (
                0.268 * epsilon))) ** -2
        except ZeroDivisionError as e:
            log.error(e)
            alt_lambda = 0
        log.info('Alternative Lambda is {}'.format(alt_lambda))
        return alt_lambda

    def line_loss(self, flow, unit):
        log.debug('Starting counting line loss\n')
        diameter = self.diameter.value * 0.001
        std_grav = 9.81
        lambda_coef = self.get_lambda(flow, unit)
        speed = self.speed(flow, unit)
        log.info('for diameter {} [m²], lambda {} [-], speed {} [m/s]'.format(
            diameter, lambda_coef, speed))
        hydraulic_gradient = (lambda_coef * (speed ** 2)) / (
            diameter * 2 * std_grav)
        log.info('hydraulic gradient is {} [-]\n'.format(hydraulic_gradient))
        line_loss = self.length.value * hydraulic_gradient
        log.info('line loss is {} [m]\n'.format(line_loss))
        return line_loss

    def local_loss(self, flow, unit):
        local_loss = ((self.speed(flow, unit) ** 2) / (2 * 9.81)) * sum(
            self.resistance.values)
        log.info('local loss is {} [m]'.format(local_loss))
        log.info('Epsilon is {}, Re is {}'.format(
            self.get_epsilon(), self.get_re(flow, unit)))
        return local_loss

    def speed(self, flow, unit):
        log.debug('input flow: {} {}'.format(flow, unit_bracket_dict[unit]))
        if unit == 'liters':
            flow *= .001
        elif unit == 'meters':
            flow /= 3600
        radius = (0.001 * self.diameter.value) / 2
        cross_sec = 3.14 * (radius ** 2)
        speed = flow / cross_sec
        log.info(
            'for flow {} [m3/s], radius {} [m], cross section {} [m2]'.format(
                flow, radius, cross_sec))
        log.info('speed is {} [m/s]'.format(speed))
        return speed

    def sum_loss(self, flow, unit):
        return self.line_loss(flow, unit) + self.local_loss(flow, unit)

    def pipe_char_ready(self):
        flag = True
        checklist = [self.length, self.diameter, self.roughness]
        for parameter in checklist:
            log.debug('{} = {}'.format(parameter, parameter.value))
            if parameter.value == 0:
                flag = False
        return flag

    def get_y_coords(self, flows, unit):
        log.debug('Getting pipe y coordinates')
        result = [self.sum_loss(flow, unit) for flow in flows]
        log.debug('Pipe loss coords: {}'.format(result))
        return result


class Pump(StationObject):
    """class for pumps"""

    def __init__(self, app):
        super().__init__(app)
        self.cycle_time = None
        self.contour = None
        self.suction_level = None
        self.efficiency_from = None
        self.efficiency_to = None
        self.characteristic = None

    def set_flow_unit(self, unit):
        log.info('set_flow_unit started')
        unit_bracket = unit_bracket_dict[unit]
        efficiency_from_label = self.ui_vars.__getitem__(
            'pump_efficiency_from_txt')
        efficiency_to_label = self.ui_vars.__getitem__(
            'pump_efficiency_to_txt')
        add_point_label = self.ui_vars.__getitem__(
            'add_point_flow_text')
        efficiency_from_label.set('Od {}'.format(unit_bracket))
        efficiency_to_label.set('Do {}'.format(unit_bracket))
        add_point_label.set('Przepływ Q {}'.format(unit_bracket))
        log.info('self.efficiency_from type: {}'.format(
            type(self.efficiency_from)))
        self.characteristic.set_unit(unit)

    def get_x_linspace(self):
        return maths.get_x_axis(self.characteristic.get_pump_char_func()[0],
                                self.efficiency_from.value,
                                self.efficiency_to.value)

    def pump_char_ready(self):
        flag = False
        if len(self.characteristic.coords) > 2:
            flag = True
        return flag

    def draw_pump_plot(self, x_lin):
        flows, lifts = self.characteristic.get_pump_char_func()
        y = maths.fit_coords(flows, lifts, 3)
        return x_lin, y(x_lin), 'b-'


class Well(StationObject):
    """class for well"""

    def __init__(self, app):
        super().__init__(app)
        self.reserve_pumps = None
        self.shape = None
        # self.set_shape(self.default['shape'])
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
        self.inflow_max = None
        self.inflow_min = None

    def set_shape(self, shape):
        self.ui_vars.__getitem__('shape').set(shape)
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

    def height_to_pump(self):
        ord_sewage_level = self.ord_inlet.value - 1.2
        result = self.ord_upper_level.value - ord_sewage_level
        return result
