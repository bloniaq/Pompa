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
        d = self.diameter.value / 1000
        return 3.14 * ((d / 2) ** 2)

    def get_epsilon(self):
        return self.roughness.value / self.diameter.value

    def get_re(self, diameter, speed):
        """Returns value of Reynolds number. Unit is none [-]
        Kinematic viscosity unit is mm2/s (water in 20 Celsius deegrees). Its
        value is constant, and provided in models.py module.
        Dividing it by 1000000 changes it unit to m2/s
        Speed should be in m/s unit, and diameter in m unit.
        """
        log.debug('diameter: {}, speed: {}, ni: {}'.format(
            diameter, speed, self.kinematic_viscosity / 1000000))
        return (diameter * speed) / (self.kinematic_viscosity / 1000000)

    def get_lambda(self, flow, re, epsilon):
        """Returns numeric value of lambda coefficient of line loss.
        Pattern used for calculation it depends on value of Reynolds number.
        """
        log.debug('re: {}'.format(re))
        if re > 0:
            lambda_gr = (-2 * np.log10((6.1 / (re ** 0.915)) + (
                0.268 * epsilon))) ** -2
        else:
            lambda_gr = 0

        def border_re(epsilon, lambda_):
            return 200 / (epsilon * (lambda_ ** 0.5))

        if re == 0:
            lambda_ = 0
        elif re <= 2320:
            lambda_ = 64 / re
        elif re < 4000:
            """strefa gwałtownego wzrostu wsp. oporów liniowych.
            Zmienny charakter ruchu, wartości nie są określone.
            Mechanika Płynów Mitoska s. 146
            """
            lambda_ = 0
        elif re < 100000:
            lambda_ = 0.3164 / (re ** 0.25)
        elif re < border_re(epsilon, lambda_gr):
            lambda_ = lambda_gr
        else:
            lambda_ = (-2 * np.log10((self.roughness.value) / (
                3.71 * self.diameter.value)))

        return lambda_

    def line_loss(self, flow):
        log.debug('Starting counting line loss\n')
        diameter = self.diameter.value * 0.001
        std_grav = 9.81
        speed = self.speed(flow)
        re = self.get_re(diameter, speed)
        epsilon = self.get_epsilon()
        lambda_ = self.get_lambda(flow, re, epsilon)
        hydraulic_gradient = (lambda_ * (speed ** 2)) / (
            diameter * 2 * std_grav)
        line_loss = self.length.value * hydraulic_gradient
        return line_loss

    def local_loss(self, flow):
        local_loss_factor = sum(self.resistance.values)
        speed = self.speed(flow)
        local_loss = ((speed ** 2) / (2 * 9.81)) * local_loss_factor
        return local_loss

    def speed(self, flow):
        """Returns value of average speed inside pipe. Unit is m/s
        """
        self.update()
        log.debug('flow m3ps: {}, area: {}'.format(flow.v_m3ps, self.area))
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
