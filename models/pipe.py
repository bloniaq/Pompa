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

    def params_for_q(self, q):
        """
        Potrzebuje przeplywu q
        Dla tego przeplywu oblicza parametry:

        I je zwraca
        """

        pass

    def get_area(self):
        d = self.diameter.value / 1000
        return 3.14 * ((d / 2) ** 2)

    def get_epsilon(self):
        epsilon = self.roughness.value / self.diameter.value
        return epsilon

    def get_re(self, flow):
        diameter = self.diameter.value
        speed = self.speed(flow)
        re = (diameter * speed) / (self.kinematic_viscosity / 1000000)
        # log.info('Reynolds number is {}'.format(re))
        return re

    def get_lambda(self, flow):
        diameter = self.diameter.value * 0.001
        epsilon = self.get_epsilon()
        log.info('Epsilon is {}'.format(epsilon))
        lambda_ = (-2 * np.log10(self.roughness.value / (
            3.71 * diameter))) ** -2
        re = self.get_re(flow)
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

    def line_loss(self, flow):
        log.debug('Starting counting line loss\n')
        diameter = self.diameter.value * 0.001
        std_grav = 9.81
        lambda_coef = self.get_lambda(flow)
        speed = self.speed(flow)
        hydraulic_gradient = (lambda_coef * (speed ** 2)) / (
            diameter * 2 * std_grav)
        # log.info('hydraulic gradient is {} [-]\n'.format(hydraulic_gradient))
        line_loss = self.length.value * hydraulic_gradient
        # log.info('line loss is {} [m]\n'.format(line_loss))
        return line_loss

    def local_loss(self, flow):
        # TODO:
        # Tests
        local_loss_factor = sum(self.resistance.values)
        speed = self.speed(flow)
        local_loss = ((speed ** 2) / (2 * 9.81)) * local_loss_factor
        # log.info('local loss is {} [m]'.format(local_loss))
        # log.info('Epsilon is {}, Re is {}'.format(
        #     self.get_epsilon(), self.get_re(flow, unit)))
        return local_loss

    def speed(self, flow):
        self.update()
        return flow.v_m3ps / self.area

    def sum_loss(self, flow):
        return self.line_loss(flow) + self.local_loss(flow)

    def pipe_char_ready(self):
        flag = True
        checklist = [self.length, self.diameter, self.roughness]
        for parameter in checklist:
            log.debug('{} = {}'.format(parameter, parameter.value))
            if parameter.value == 0:
                flag = False
        return flag

    def get_y_coords(self, flows):
        log.debug('Getting pipe y coordinates')
        result = [self.sum_loss(flow) for flow in flows]
        log.debug('Pipe {} loss coords: {}'.format(self, result))
        return result

    def get_pipe_char_vals(self, station, unit):
        log.debug('Starting getting pipe vals')
        flows, _ = station.pump.characteristic.get_pump_char_func(1)
        flows_vals = [flow.ret_unit(unit) for flow in flows]
        y_coords = self.get_y_coords(flows)
        pipes_char = []
        for i in range(len(flows)):
            sum_l = y_coords[i]
            log.debug('####################\n\n')
            log.debug('flow: {}, pipe: {}, sum: {}'.format(
                flows_vals[i], y_coords[i], sum_l))
            log.debug('\n####################\n\n')
            pipes_char.append(sum_l)
        y = self.app.fit_coords(flows_vals, pipes_char, 2)
        log.debug('Finding ys finished')
        return y
