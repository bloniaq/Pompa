from exceptions import InputTypeError


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

    def __eq__(self, other):
        return (self.value_m3ph == other.value_m3ph)

    def set(self, value, unit='m3ph'):
        try:
            if unit == 'm3ph':
                self.value_m3ph = round(value, 2)
                self.value_lps = self._lps(value)
            elif unit == 'lps':
                self.value_lps = round(value, 2)
                self.value_m3ph = self._m3ph(value)
        except (ValueError, TypeError):
            raise InputTypeError
        else:
            super().set(None)

    def _lps(self, m3ph):
        return round(m3ph / 3.6, 2)

    def _m3ph(self, lps):
        return round(lps * 3.6, 2)


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


class PumpCharVariable(Variable):
    '''Holds pump characteristic'''

    def __init__(self):
        self.value = []
        super().__init__(self.value)

    def add_point(self, flow, height, unit='m3ph'):
        point = (FlowVariable(flow, unit), height)
        self.value.append(point)

    def remove_point(self, point):
        self.value.remove(point)

    def sort_points(self):
        self.value.sort(key=lambda point: point[0].value_m3ph)
