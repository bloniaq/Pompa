import math
import pompa.models.variables as v
import numpy as np
from pompa.exceptions import FrictionFactorMethodOutOfRange


class Pipe(v.StationObject):
    """Class used for keep pipe used in station

    Attributes
    ----------
    length : FloatVariable
        Lenght of pipe [m]
    diameter : FloatVariable
        Diameter of pipe [m]
    roughness : FloatVariable
        Value of pipe roughness [m]
    resistance : ResistanceVariable
        Values of local resistances [-]

    Methods
    -------
    area
        Returns corss-sectional area of pipe [m²]
    sum_loss(flow)
        Returns sum of line and local loss for passed flow
    dynamic_loss_polynomial(min_inflow, max_inflow, parallels=1)
        Returns polynomial of dynamic loss function of pipe
    """

    def __init__(self):
        self.length = v.FloatVariable()
        self.diameter = v.FloatVariable(digits=3)
        self.roughness = v.FloatVariable(digits=7)
        self.resistance = v.ResistanceVariable()

    def area(self):
        """Calculate cross-sectional area of pipe"""

        return round((3.14 * ((self.diameter.value / 2) ** 2)), 4)

    def _velocity(self, flow):
        """Return value of average velocity inside pipe.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Speed [m/s]
        """

        return round(flow.value_m3ps / self.area(), 4)

    def _reynolds(self, flow):
        """Return Reynolds number.

        Kinematic viscosity unit is m2/s (water in 20 Celsius deegrees). Its
        value is constant, and provided in models.py module.
        velocity should be in m/s unit, and diameter in m unit.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Reynolds number unit is none [-]
        """

        return round(((self.diameter.value) * self._velocity(flow)) / (
            self.kinematic_viscosity))

    def _lambda(self, re):
        """Return numeric value of lambda coefficient of line loss.

        Parameters
        ----------
        re : float
            Reynolds number

        Returns
        -------
        float
            lambda coefficient
        """

        lambda_ = FrictionFactor(self.diameter, self.roughness, re)(
            method='bellos-nalbantis-tsakiris')
        return round(lambda_, 4)

    def _hydraulic_gradient(self, flow):
        """Calculate hydraulic gradient of losses.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Hydraulic gradient
        """

        return (self._lambda(self._reynolds(flow)) * (
            self._velocity(flow) ** 2)) / ((
                self.diameter.value) * 2 * self.std_grav)

    def _line_loss(self, flow):
        """Calculate line loss.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Line loss
        """

        return round(self.length.value * self._hydraulic_gradient(flow), 3)

    def _local_loss(self, flow):
        """Calculate local loss.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Local loss
        """

        return round(((self._velocity(flow) ** 2) / (
            2 * self.std_grav)) * self.resistance.sum(), 2)

    def sum_loss(self, flow):
        """Calculate sum of losses.

        Parameters
        ----------
        flow : FlowVariable
            Checked flow in pipe

        Returns
        -------
        float
            Sum of losses
        """

        return self._line_loss(flow) + self._local_loss(flow)

    def dynamic_loss_polynomial(self, min_inflow, max_inflow, parallels=1):
        """Calculate polynomial coefficients of dynamic loss in pipe.

        Coefficients are calculates based on losses values and flows multiplied
        by number of parallel pipes

        Parameters
        ----------
        min_inflow : FlowVariable
            Minimal inflow of station
        max_inflow : FlowVariable
            Maximal inflow of station
        parallels : int, optional
            Number of parallel pipes

        Returns
        -------
        numpy.ndarray
            Coefficients of losses polynomial function
        """
        flows_array = np.linspace(
            min_inflow.value_m3ps, 1.4 * max_inflow.value_m3ps, 20)

        heights_list = []

        for flow_val in flows_array:
            loss = self.sum_loss(v.FlowVariable(flow_val, 'm3ps'))
            heights_list.append(round(loss, 3))

        heights_array = np.array(heights_list)

        flows_array *= parallels

        coeffs = np.polynomial.polynomial.polyfit(
            flows_array, heights_array, 2)

        coeffs = np.append(coeffs, 0)

        return coeffs


class FrictionFactor:
    """Class used for Darcy friction factor calculations.

    Each effective method (enumerated in methods dictionary)
    """

    def __init__(self, diameter, roughness, reynolds, precision=4):
        """
        diameter  - [m] - D                - diameter of pipe
        reynolds  - [-] - Re               - Reynolds number
        roughness - [m] - ε (int.), k (PL) - absolute roughness
        """
        self._diameter = diameter.value
        self._roughness = roughness.value
        self._reynolds = reynolds

        self._precision = precision
        self._methods = {
            'colebrook-white': self._colebrook_white,
            'walden': self._walden,
            'hagen-poiseuille': self._hagen_poiseuille,
            'blasius': self._blasius,
            'haaland': self._haaland,
            'bellos-nalbantis-tsakiris': self._bnt,
            'cheng': self._cheng,
            'wood': self._wood,
            'swamee-jain': self._swamee_jain,
            'churchill': self._churchill,
            'mitosek': self._mitosek
        }

    def __call__(self, method='colebrook-white'):
        return self._methods[method]()

    def __comparision(self, print_errors=False, in_range_only=False,
                      compare_value=None):
        """ This method is mainly for diagnostic and is helpful on figuring out
        algorythm of previous version of application. It returns dict of all
        existing methods results, no matter of range"""
        results = {}
        errors = []
        print('***** INPUTDATA *****')
        print('Diameter        : ', self._diameter, 'm')
        print('Roughness       : ', self._roughness, 'm')
        print('Reynolds Number : ', self._reynolds)
        print('\n*****  RESULTS  *****')
        for method in self._methods.keys():
            try:
                results[method] = self._methods[method]()
            except FrictionFactorMethodOutOfRange as e:
                if not in_range_only:
                    results[method] = (
                        round(e.value, self._precision), 'OUT OF RANGE')
                    print(f'{f"{method}":<30}{f"{results[method][0]}":<10}{f"{results[method][1]}"}')
                    errors.append(e.error)
                continue
            else:
                print(f'{f"{method}":<30}{f"{results[method]}":<10}')

        if print_errors:
            print('\n*****   ERRORS  *****')
            for e in errors:
                print(e)

        if compare_value:
            print('\n***** TO COMPARE *****')
            print(f'{f"compare value":<30}{f"{compare_value}":<10}')

        return results

    def __raise_out_of_range(self, method, value):
        raise FrictionFactorMethodOutOfRange(
            self._methods[method].__func__.__doc__, self._diameter,
            self._roughness, self._reynolds, value)

    # METHODS

    def _colebrook_white(self):
        """
        Colebrook-White equation
        Range:
            4000 < Re
        """
        cw_friction = 0.9
        reynolds = self._reynolds
        enough_close = False
        while not enough_close:
            leftF = 1 / cw_friction ** 0.5
            rightF = - 2 * math.log10(2.51 / (
                reynolds * cw_friction ** 0.5) + (self._roughness) / (
                    3.72 * self._diameter))
            cw_friction -= 0.000001
            if (rightF - leftF <= 0):  # Check if Left = Right
                enough_close = True

        if self._reynolds < 4000:
            self.__raise_out_of_range('colebrook-white', cw_friction)

        return round(cw_friction, self._precision)

    def _walden(self):
        """
        Walden approximation.
        Walden H.: Mechanika Płynów. WPW, Warszawa 1986
        Range:
            100000 < Re
        """
        walden = (-2 * np.log10((6.1 / (self._reynolds ** 0.915)) + (
            0.268 * (self._roughness / self._diameter)))) ** -2

        if self._reynolds < 100000:
            self.__raise_out_of_range('walden', walden)

        return round(walden, self._precision)

    def _hagen_poiseuille(self):
        """
        Hagen–Poiseuille equation
        1838, 1840
        Range:
            Re < 2300
        """
        hag_pois = 64 / self._reynolds

        if self._reynolds > 2300:
            self.__raise_out_of_range('hagen-poiseuille', hag_pois)

        return round(hag_pois, self._precision)

    def _blasius(self):
        """
        Blasius approximation
        1913
        Range:
            4000 < Re < 100000
        """
        blasius = 0.3164 / (self._reynolds ** 0.25)

        if not 4000 <= self._reynolds <= 100000:
            self.__raise_out_of_range('blasius', blasius)

        return round(blasius, self._precision)

    def _wood(self):
        """
        Wood approximation
        1966
        Range:
            4000 < Re < 50000000
            0.00001 < roughness/diameter < 0.04
        """
        rel_roughness = self._roughness / self._diameter
        psi = 1.62 * (rel_roughness ** 0.134)
        comp_1 = 0.094 * (rel_roughness ** 0.225)
        comp_2 = 0.53 * rel_roughness
        comp_3 = 88 * (rel_roughness ** 0.44) * (self._reynolds ** (-1 * psi))
        wood = comp_1 + comp_2 + comp_3

        if not (4000 < self._reynolds < 50000000 and
                0.00001 < rel_roughness < 0.04):
            self.__raise_out_of_range('wood', wood)

        return round(wood, self._precision)

    def _swamee_jain(self):
        """
        Swamee and Jain approximation
        1976
        Range:
            5000 < Re < 100000000
            0.000001 < roughness/diameter < 0.05
        """
        rel_roughness = self._roughness / self._diameter

        swamee_jain = 0.25 / ((math.log10((rel_roughness / 3.7) + (5.74 / (
            self._reynolds ** 0.9)))) ** 2)

        if not (5000 < self._reynolds < 100000000 and
                0.000001 < rel_roughness < 0.05):
            self.__raise_out_of_range('swamee-jain', swamee_jain)

        return round(swamee_jain, self._precision)

    def _churchill(self):
        """
        Churchill approximation
        1977
        Range:
            All Flow Regimes
        """
        factor_1 = (-2.457 * math.log(((7 / self._reynolds) ** 0.9) + (
            0.27 * self._roughness / self._diameter))) ** 16
        factor_2 = (37530 / self._reynolds) ** 16
        churchill = 8 * ((((8 / self._reynolds) ** 12) + (1 / ((
            factor_1 + factor_2) ** 1.5))) ** (1 / 12))

        return round(churchill, self._precision)

    def _haaland(self):
        """
        Haaland approximation
        1983
        Range:
            4000 < Re
        """
        haaland = (-1.8 * np.log10((
            self._roughness / (3.7 * self._diameter)) ** 1.11 + (
                6.9 / self._reynolds))) ** -2

        if self._reynolds < 4000:
            self.__raise_out_of_range('haaland', haaland)

        return round(haaland, self._precision)

    def _cheng(self):
        """
        Cheng approximation
        2008
        Range:
            All Flow Regimes
        """
        coeff_a = 1 / (1 + ((self._reynolds / 2720) ** 9))
        coeff_b = 1 / (1 + ((self._reynolds / (160 * (
            self._diameter / self._roughness))) ** 2))
        factor_1 = (self._reynolds / 64) ** coeff_a
        factor_2 = (1.8 * math.log10(self._reynolds / 6.8)) ** (
            2 * (1 - coeff_a) * coeff_b)
        factor_3 = (2 * math.log10(
            3.7 * self._diameter / self._roughness)) ** (
                2 * (1 - coeff_a) * (1 - coeff_b))
        cheng = 1 / (factor_1 * factor_2 * factor_3)
        return round(cheng, self._precision)

    def _bnt(self):
        """
        Bellos, Nalbantis, Tsakris approximation
        2018
        https://www.sciencedirect.com/science/article/pii/S0029549311000173
        Range:
            All Flow Regimes
        """
        coeff_a = 1 / (1 + ((self._reynolds / 2712) ** 8.4))
        coeff_b = 1 / (1 + ((self._reynolds / (150 * (
            self._diameter / self._roughness))) ** 1.8))
        factor_1 = (64 / self._reynolds) ** coeff_a
        factor_2 = (0.75 * math.log(self._reynolds / 5.37)) ** (
            2 * (coeff_a - 1) * coeff_b)
        factor_3 = (0.88 * math.log(3.41 * (
            self._diameter / self._roughness))) ** (
                2 * (coeff_a - 1) * (1 - coeff_b))
        bnt = factor_1 * factor_2 * factor_3
        return round(bnt, self._precision)

    def _mitosek(self):
        """Return numeric value of lambda coefficient of line loss.

        Pattern used for calculation it depends on value of Reynolds number.
        """

        def _boundary_lambda():
            if self._reynolds > 0:
                lambda_boundary = (-2 * np.log10((6.1 / (
                    self._reynolds ** 0.915)) + (
                        0.268 * _epsilon()))) ** -2
            else:
                lambda_boundary = 0
            return round(lambda_boundary, 4)

        def _boundary_reynolds(_lambda):
            return round(200 / (_epsilon() * (_lambda ** 0.5)))

        def _epsilon():
            return round(self._roughness / self._diameter, 4)

        if self._reynolds == 0:
            lambda_ = 0
        elif self._reynolds <= 2320:
            lambda_ = 64 / self._reynolds
        elif self._reynolds < 4000:
            """strefa gwałtownego wzrostu wsp. oporów liniowych.
            Zmienny charakter ruchu, wartości nie są określone.
            Mechanika Płynów Mitoska s. 146
            """
            lambda_ = 0
        elif self._reynolds <= 100000:
            lambda_ = 0.3164 / (self._reynolds ** 0.25)
        elif self._reynolds < _boundary_reynolds(_boundary_lambda()):
            lambda_ = self._boundary_lambda()
        else:
            lambda_ = (-2 * np.log10((self._roughness) / (
                3.71 * self._diameter))) ** -2

        return round(lambda_, 4)
