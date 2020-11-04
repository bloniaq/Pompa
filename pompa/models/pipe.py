import models.station_obj as station_object
import models.variables as v
import numpy as np


class Pipe(station_object.StationObject):
    '''
    Keeps pipe attrubutes:
    - lenght[m]
    - diameter [m]
    - roughness [m]
    - resistance [-]
    - parallels [-]

    Methods returns units:
    - area [m²]
    - epsilon [-]
    - speed [m/s]
    '''

    def __init__(self):
        self.length = v.FloatVariable()
        self.diameter = v.FloatVariable(digits=3)
        self.roughness = v.FloatVariable(digits=6)
        self.resistance = v.ResistanceVariable()
        self.parallels = v.IntVariable()

    def area(self):
        return round((3.14 * ((self.diameter.value / 2) ** 2)), 4)

    def _epsilon(self):
        return round(self.roughness.value / self.diameter.value, 4)

    def _speed(self, flow):
        '''
        Returns value of average speed inside pipe. Expects FlowVariable.
        Result unit is m/s
        '''

        return round((flow.value_m3ph / 3600) / self.area(), 4)

###

    def _reynolds_n(self, flow):
        """Returns value of Reynolds number. Unit is none [-]
        Kinematic viscosity unit is m2/s (water in 20 Celsius deegrees). Its
        value is constant, and provided in models.py module.
        Speed should be in m/s unit, and diameter in m unit.
        """
        return round(((self.diameter.value) * self._speed(flow)) / (
            self.kinematic_viscosity))

    def _boundary_lambda(self, re):
        if re > 0:
            lambda_boundary = (-2 * np.log10((6.1 / (re ** 0.915)) + (
                0.268 * self._epsilon()))) ** -2
        else:
            lambda_boundary = 0
        return round(lambda_boundary, 4)

    def _boundary_reynolds_n(self, _lambda):
        return round(200 / (self._epsilon() * (_lambda ** 0.5)))

    def _lambda(self, re):
        """Returns numeric value of lambda coefficient of line loss.
        Pattern used for calculation it depends on value of Reynolds number.
        """
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
        elif re <= 100000:
            lambda_ = 0.3164 / (re ** 0.25)
        elif re < self._boundary_reynolds_n(self._boundary_lambda(re)):
            lambda_ = self._boundary_lambda(re)
        else:
            lambda_ = (-2 * np.log10((self.roughness.value) / (
                3.71 * self.diameter.value))) ** -2

        return round(lambda_, 4)

    def _hydraulic_gradient(self, flow):
        return (self._lambda(self._reynolds_n(flow)) * (
            self._speed(flow) ** 2)) / ((
                self.diameter.value) * 2 * self.std_grav)

    def _line_loss(self, flow):
        return round(self.length.value * self._hydraulic_gradient(flow), 3)

    def _local_loss(self, flow):
        return round(((self._speed(flow) ** 2) / (
            2 * self.std_grav)) * self.resistance.sum(), 2)

    def sum_loss(self, flow):
        return self._line_loss(flow) + self._local_loss(flow)
