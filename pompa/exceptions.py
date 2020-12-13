import matplotlib.pyplot as plt
import numpy as np


class InputTypeError(ValueError):
    pass


class TooManyRootsError(ValueError):
    def __init__(self, roots, pipeset_poly, pumpset_poly):
        print('Too many roots: ', roots)
        print('pipeset_poly: ', pipeset_poly)
        print('pumpset_poly: ', pumpset_poly)


class NoRootsError(ValueError):
    def __init__(self, roots, pipeset_poly, pumpset_poly, min_inflow,
                 max_inflow):
        sum_pipes_f = np.polynomial.polynomial.Polynomial(pipeset_poly)
        pumps_f = np.polynomial.polynomial.Polynomial(pumpset_poly)
        x = np.linspace(min_inflow.value_m3ps, max_inflow.value_m3ps, num=1000)
        plt.plot(x, pumps_f(x), 'b-')
        plt.plot(x, sum_pipes_f(x), 'g-')
        plt.show()


class WellTooShallowError(Exception):
    pass


class WellTooDeepError(Exception):
    pass


class FrictionFactorMethodOutOfRange(Exception):
    def __init__(self, docstring, diameter, roughness, reynolds, value):
        self.value = value
        self.error = ''
        self.error += docstring
        self.error += '\nReynolds Number : ' + str(reynolds)
        self.error += '\nRoughness :       ' + str(roughness)
        self.error += '\nDiameter :        ' + str(diameter) + '\n'
