import matplotlib.pyplot as plt
import numpy as np


class ErrorContainer:
    # Singleton

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.errors = []
        return cls._instance

    def add_error(self, error):
        self.errors.append(error)

    def get_errors(self):
        return self.errors

    def clear_errors(self):
        self.errors = []


class Registration:

    def __init__(self):
        errors = ErrorContainer()
        errors.add_error(self)
        self.critical_flag = False

    def get_message(self):
        message = "Błąd" + self
        return message

class InputTypeError(ValueError):
    pass


class TooManyRootsError(ValueError, Registration):
    def __init__(self, roots, pipeset_poly, pumpset_poly):
        Registration.__init__(self)
        self.critical_flag = True
        print('Too many roots: ', roots)
        print('pipeset_poly: ', pipeset_poly)
        print('pumpset_poly: ', pumpset_poly)

    def get_message(self):
        message = "Błędny kształt charakterystyki pompy. Należy poprawić " \
                  "wprowadzone dane lub skorzystać z opcji poprawki"
        return message


class NoRootsError(ValueError):
    def __init__(self, roots, pipeset_poly, pumpset_poly, min_inflow,
                 max_inflow):
        sum_pipes_f = np.polynomial.polynomial.Polynomial(pipeset_poly)
        pumps_f = np.polynomial.polynomial.Polynomial(pumpset_poly)
        x = np.linspace(min_inflow.value_m3ps, max_inflow.value_m3ps, num=1000)
        plt.plot(x, pumps_f(x), 'b-')
        plt.plot(x, sum_pipes_f(x), 'g-')
        plt.show()


class WellTooShallowError(Exception, Registration):
    def __init__(self, ordinate, ord_inlet, c_time, pump_no):
        Registration.__init__(self)
        self.critical_flag = True

        self.ordinate = ordinate
        self.ord_inlet = ord_inlet
        self.c_time = c_time
        self.pump_no = pump_no

    def get_message(self):
        message = f"Obliczenia czasu cyklu dla danych parametrów studni nie " \
                  f"powiodły się."
        return message


class WellTooDeepError(Exception):
    pass


class NotEnoughPointsInPumpCharError(Exception, Registration):
    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = True

    def get_message(self):
        message = f"Niewystarczająca liczba punktów charakterystyki pompy"
        return message


class NotEnouthDataInPipeCharError(Exception, Registration):
    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = True

    def get_message(self):
        message = "Niewystarczająca ilość danych dla charakterystyki przewodów"
        return message


class IdealSmoothnessPipeError(Exception, Registration):
    def __init__(self, error):
        Registration.__init__(self)
        self.error = error
        print(error)
        self.critical_flag = True

    def get_message(self):
        message = "Nie wprowadzono parametru chropowatości co najmniej " \
                  "jednego z przewodów"
        return message


class InfiniteWorkingTimeError(Exception, Registration):

    def __init__(self, pumps_no):
        Registration.__init__(self)
        self.pumps_no = pumps_no
        self.critical_flag = False

    def get_message(self):
        if self.pumps_no == 1:
            message = "Nie udało się obliczyć czasu pracy pojedynczej pompy"
        else:
            message = "Nie udało się obliczyć czasu pracy zestawu" \
                      f" {self.pumps_no} współpracujących pomp"
        return message


class NoPumpsetError(Exception, Registration):

    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = False

    def get_message(self):
        message = "Nie udało się przeprowadzić poprawnych obliczeń dla ani " \
                  "jednej pracującej pompy. Niewystarczające dane pompy."
        return message


class WellTooSmallError(Exception, Registration):

    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = False

    def get_message(self):
        message = "Studnia ma zbyt małą powierzchnię, żeby pomieścić dobraną" \
                  " liczbę pomp."
        return message


class InletInDeadVolumeError(Exception, Registration):

    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = False

    def get_message(self):
        message = "Dno przewodu doprowadzającego ścieki poniżej rzędnej " \
                  "wierzchu objętości martwej pompowni"
        return message


class InsidePipesTooShortError(Exception, Registration):

    def __init__(self):
        Registration.__init__(self)
        self.critical_flag = False

    def get_message(self):
        message = "Podano zbyt małą długość przewodów wewnętrznych wobec " \
                  "podanych rzędnych"
        return message


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

