from pompa.exceptions import InputTypeError
import numpy as np


class Variable():
    '''Abstract class responsible for provide interface of a model variable
    '''

    def __init__(self, value=None):
        self.value = value
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = None

    def _callbacks(self):
        for func in self.callbacks:
            func(self.value)

    def set(self, value):
        self.value = value
        self._callbacks()

    def get(self):
        return self.value


class FloatVariable(Variable):
    '''Holds variables needed to be represent in decimal numbers
    '''

    def __init__(self, value=0.0, digits=2):
        self.digits = digits
        value = self._round(value)
        super().__init__(value)

    def __repr__(self):
        return str(self.value) + ' FV'

    def __add__(self, other):
        if isinstance(other, FloatVariable):
            return FloatVariable(self.value + other.value)
        else:
            return FloatVariable(self.value + other)

    def __sub__(self, other):
        if isinstance(other, FloatVariable):
            return FloatVariable(self.value - other.value)
        else:
            return FloatVariable(self.value - other)

    def __truediv__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value / other.value)
        else:
            return FloatVariable(self.value / other, self.digits)

    def __eq__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value == other.value)
        else:
            return (self.value == other)

    def __lt__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value < other.value)
        else:
            return (self.value < other)

    def __le__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value <= other.value)
        else:
            return (self.value <= other)

    def __gt__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value > other.value)
        else:
            return (self.value > other)

    def __ge__(self, other):
        if isinstance(other, FloatVariable):
            return (self.value >= other.value)
        else:
            return (self.value >= other)

    def set(self, value):
        value = self._round(value)
        super().set(value)

    def _round(self, value):
        try:
            value = float(round(value, self.digits))
        except (ValueError, TypeError):
            raise InputTypeError
        else:
            return value


class IntVariable(Variable):
    '''Holds variables needed to be represent in integers
    '''

    def __init__(self, value=0):
        value = self._round(value)
        super().__init__(value)

    def set(self, value):
        value = self._round(value)
        super().set(value)

    def _round(self, value):
        try:
            value = value = int(round(value))
        except (ValueError, TypeError):
            raise InputTypeError()
        else:
            return value


class FlowVariable(Variable):
    '''Holds variables which keep flow values, and provide unit conversion
    '''

    def __init__(self, value=0, unit='m3ph'):
        super().__init__()
        self.set(value, unit)
        self.init_unit = unit

    def __repr__(self):
        return '{} lps'.format(self.value_lps)

    def __eq__(self, other):
        return (self.value_m3ph == other.value_m3ph)

    def __lt__(self, other):
        return (self.value_m3ph < other.value_m3ph)

    def __le__(self, other):
        return (self.value_m3ph <= other.value_m3ph)

    def __gt__(self, other):
        return (self.value_m3ph > other.value_m3ph)

    def __ge__(self, other):
        return (self.value_m3ph >= other.value_m3ph)

    def __add__(self, other):
        return FlowVariable(self.value_m3ph + other.value_m3ph)

    def __sub__(self, other):
        return FlowVariable(self.value_m3ph - other.value_m3ph)

    def __truediv__(self, other):
        if isinstance(other, FlowVariable):
            return (self.value_m3ph / other.value_m3ph)
        else:
            return FlowVariable(self.value_m3ph / other, 'm3ph')

    def __floordiv__(self, other):
        return (self.value_m3ph // other.value_m3ph)

    def set(self, value, unit='m3ph'):
        try:
            if unit == 'm3ph':
                self.value_m3ph = round(value, 2)
                self.value_lps = self._lps(value)
            elif unit == 'lps':
                self.value_lps = round(value, 2)
                self.value_m3ph = self._m3ph(value)
            elif unit == 'm3ps':
                self.set(value * 1000, 'lps')
            self.value_m3ps = self._m3ps(self.value_lps)
        except (ValueError, TypeError):
            raise InputTypeError
        else:
            super().set(None)

    def _lps(self, m3ph):
        return round(m3ph / 3.6, 2)

    def _m3ph(self, lps):
        return round(lps * 3.6, 2)

    def _m3ps(self, lps):
        return round(lps / 1000, 5)


class SwitchVariable(Variable):
    '''Holds variables which keep switchable things'''

    def __init__(self, value='', dictionary={}):
        super().__init__(value)
        self.dictionary = dictionary


class ResistanceVariable(Variable):
    '''Holds list of resistance coefficients'''

    def __init__(self, value=[]):
        super().__init__(value)

    def sum(self):
        return sum(self.value)

    def set(self, value):
        if isinstance(value, list):
            super().set(value)
        else:
            super().set([value])


class PumpCharVariable(Variable):
    '''Holds pump characteristic'''

    def __init__(self):
        self.value = []
        super().__init__(self.value)

    def __repr__(self):
        return str(self.value)

    def add_point(self, flow, height, unit='m3ph'):
        point = (FlowVariable(flow, unit), height)
        self.value.append(point)
        self._sort_points()
        self._callbacks()

    def remove_point(self, point):
        self.value.remove(point)

    def _sort_points(self):
        self.value.sort(key=lambda point: point[0].value_m3ph)

    def polynomial_coeff(self, w_pumps_amount=1):
        flows = np.array(
            [w_pumps_amount * f[0].value_m3ps for f in self.value])
        heights = np.array([h[1] for h in self.value])
        print('poly flows: ', flows)
        print('poly heights: ', heights)
        return np.polynomial.polynomial.polyfit(flows, heights, 3)
