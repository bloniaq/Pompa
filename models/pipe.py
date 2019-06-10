# libraries
import logging
import numpy as np

# modules
import models.models as models

log = logging.getLogger('pompa.pipe')


class Pipe(models.StationObject):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)

        # input parameters
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = 0
        self.parallels = 1

        # parameters to calculate
        self.area = 0
        self.epsilon = 0

    def update(self):
        self.area = self.get_area()
        self.epsilon = self.get_epsilon()

    def get_area(self):
        return 3.14 * ((self.diameter.value / 2) ** 2)

    def get_epsilon(self):
        diameter = self.diameter.value
        epsilon = self.roughness.value / diameter
        return epsilon

    def get_re(self, flow, unit):
        diameter = self.diameter.value
        speed = 1000 * self.speed(flow, unit)
        re = (diameter * speed) / self.kinematic_viscosity
        # log.info('Reynolds number is {}'.format(re))
        return re

    def get_lambda(self, flow, unit):
        diameter = self.diameter.value * 0.001
        epsilon = self.get_epsilon()
        log.info('Epsilon is {}'.format(epsilon))
        lambda_ = (-2 * np.log10(self.roughness.value / (
            3.71 * diameter))) ** -2
        re = self.get_re(flow, unit)
        # log.info('Re is {}'.format(re))
        # log.info('Lambda is {}'.format(lambda_))
        try:
            alt_lambda = (-2 * np.log10((6.1 / (re ** 0.915)) + (
                0.268 * epsilon))) ** -2
        except ZeroDivisionError as e:
            log.error(e)
            alt_lambda = 0
        # log.info('Alternative Lambda is {}'.format(alt_lambda))
        return alt_lambda

    def line_loss(self, flow, unit):
        log.debug('Starting counting line loss\n')
        diameter = self.diameter.value * 0.001
        std_grav = 9.81
        lambda_coef = self.get_lambda(flow, unit)
        speed = self.speed(flow, unit)
        hydraulic_gradient = (lambda_coef * (speed ** 2)) / (
            diameter * 2 * std_grav)
        # log.info('hydraulic gradient is {} [-]\n'.format(hydraulic_gradient))
        line_loss = self.length.value * hydraulic_gradient
        # log.info('line loss is {} [m]\n'.format(line_loss))
        return line_loss

    def local_loss(self, flow, unit):
        # TODO:
        # Tests
        local_loss_factor = sum(self.resistance.values)
        speed = self.speed(flow, unit)
        local_loss = ((speed ** 2) / (2 * 9.81)) * local_loss_factor
        # log.info('local loss is {} [m]'.format(local_loss))
        # log.info('Epsilon is {}, Re is {}'.format(
        #     self.get_epsilon(), self.get_re(flow, unit)))
        return local_loss

    def speed(self, flow, unit):
        # log.debug('input flow: {} {}'.format(flow, unit_bracket_dict[unit]))
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
        # log.info('speed is {} [m/s]'.format(speed))
        return speed

    def sum_loss(self, flow, unit='liters'):
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

    def get_pipe_char_vals(self, station, unit):
        log.debug('Starting getting pipe vals')
        flows, _ = station.pump.characteristic.get_pump_char_func(unit)
        y_coords = self.get_y_coords(flows, unit)
        log.debug('Got ys')
        pipes_char = []
        for i in range(len(flows)):
            sum_l = y_coords[i]
            log.debug('####################\n\n')
            log.debug('flow: {}, pipe: {}, sum: {}'.format(
                flows[i], y_coords[i], sum_l))
            log.debug('\n####################\n\n')
            pipes_char.append(sum_l)
        y = self.app.fit_coords(flows, pipes_char, 2)
        log.debug('Finding ys finished')
        return y
