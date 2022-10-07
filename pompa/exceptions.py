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
    def __init__(self, ordinate, ord_inlet, c_time, pump_no):
        print('Cycle Time {} is too short at {} and st. inlet is at {}'.format(
            c_time, ordinate, ord_inlet))
        print('pump no: ', pump_no)


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


class UnsupportedOperationError(ValueError):
    def __init__(self, operation):
        print(f"Operation {operation} is not supported")


class NoSuchVariableError(AttributeError):
    def __init__(self, name):
        print(f"There's no Variable named <<{name}>> in model")


class DuplicatedVariableError(AttributeError):
    def __init__(self, name, variables):
        print(f"There's more than one Variable with <<{name}>> name in model")
        print("all variables:")
        for v in variables:
            print(f"Name: {v.name}\t\tValue: {v.value}")

class BrokenDataError(Exception):
    def __init__(self):
        print("loaded file has broken or incomplete data")

