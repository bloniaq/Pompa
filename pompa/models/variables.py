from pompa.exceptions import InputTypeError, UnsupportedOperationError
import numpy as np


class StationObject:
    """Abstract class for subclassing Station objects.

    Providing interface for loading values from file

    Methods
    -------
    load_data(data_dict)

    """

    kinematic_viscosity = 0.0000010068  # [m²/s] dla 20°C
    std_grav = 9.81

    def __init__(self):
        pass

    def __setattr__(self, attr, value):
        if '.' not in attr:
            self.__dict__[attr] = value
        else:
            attr_name, rest = attr.split('.', 1)
            setattr(getattr(self, attr_name), rest, value)

    def __getattr__(self, attr):
        if '.' not in attr:
            try:
                return super().__getattr__(attr)
            except AttributeError as e:
                raise AttributeError(e)
        else:
            attr_name, rest = attr.split('.', 1)
            return getattr(getattr(self, attr_name), rest)

    def load_data(self, data_dict):
        for attribute in self.__dict__:
            if hasattr(self.__dict__[attribute], 'dan_id'):
                self.__dict__[attribute].load_data(data_dict)


class Variable:
    """Abstract class responsible for provide interface of a model variable."""

    instances = []

    def __init__(self, value=None, name=None):
        self.name = name
        self.value = value
        self.callbacks = {}
        self._var_register()

    def _var_register(self):
        """
        Appends self instance to class attribute list of all instances if name
        attribute is specified.
        In case of finding same-named instance in the list, it pops it

        WARNING!
        There is assumption, that list of instances is useless for variables
        without name attribute specified. There are only non-None named
        instances on the instances list.

        :return: None
        """
        indexes_to_pop = []
        for i in range(len(Variable.instances)):
            var = Variable.instances[i]
            if var.name == self.name:
                indexes_to_pop.insert(0, i)
        for i in indexes_to_pop:
            Variable.instances.pop(i)
        if self.name is not None:
            Variable.instances.append(self)

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

    @classmethod
    def get_var(cls, name):
        return [var for var in cls.instances if var.name == name][-1]


class FloatVariable(Variable):
    """Holds variables needed to be represent in decimal numbers"""

    def __init__(self, value=0.0, digits=2, name=None):
        self.digits = digits
        value = self._round(value)
        super().__init__(value, name)

    def __str__(self):
        return str(self.value) + ' FV'

    def __repr__(self):
        return str(self.name) + ": " + str(self.value) + ' FV'

    def __add__(self, other):
        if isinstance(other, FloatVariable):
            self.set(self.value + other.value)
            return self
        else:
            self.set(self.value + other)
            return self

    def __sub__(self, other):
        if isinstance(other, FloatVariable):
            self.set(self.value - other.value)
            return self
        else:
            self.set(self.value - other)
            return self

    def __mul__(self, other):
        if isinstance(other, FloatVariable):
            self.set(self.value * other.value)
            return self
        else:
            self.set(self.value * other)
            return self

    def __truediv__(self, other):
        if isinstance(other, FloatVariable):
            self.set(self.value / other.value)
            return self
        else:
            self.set(self.value / other)
            return self

    def __eq__(self, other):
        if isinstance(other, FloatVariable):
            return self.value == other.value
        else:
            return self.value == other

    def __lt__(self, other):
        if isinstance(other, FloatVariable):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other):
        if isinstance(other, FloatVariable):
            return self.value <= other.value
        else:
            return self.value <= other

    def __gt__(self, other):
        if isinstance(other, FloatVariable):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, FloatVariable):
            return self.value >= other.value
        else:
            return self.value >= other

    def __round__(self, digits):
        # return FloatVariable(round(self.value, digits))
        if digits is None:
            digits = self.digits
        self.value.__round__(digits)
        return self

    def set(self, value):
        value = self._round(value)
        super().set(value)

    def _round(self, value):
        # TODO: Nie podoba mi się ta metoda
        try:
            value = float(round(value, self.digits))
        except (ValueError, TypeError):
            raise InputTypeError
        else:
            return value

    def copy(self):
        if self.name is not None:
            self.name += "-copy"
        return FloatVariable(self.value, self.digits, self.name)


class IntVariable(Variable, int):
    """Class used to combine int values and tk-oriented callbacks interface"""

    # def __new__(self, value=0):
    #     return int.__new__(self, value)
    #     self.value = self

    def __init__(self, value=0, name=None):
        value = self._round(value)
        super().__init__(value, name)
        self.value = self

    def set(self, value):
        value = self._round(value)
        super().set(value)

    def _round(self, value):
        # TODO: Nie podoba mi się ta metoda
        try:
            value = value = int(round(value))
        except (ValueError, TypeError):
            raise InputTypeError()
        else:
            return value

class FlowVariable(Variable):
    """Holds variables which keep flow values, and provide unit conversion"""

    def __init__(self, value=0, unit='m3ph', name=None):
        super().__init__(name=name)
        self.set(value, unit)
        self.base_unit = unit

    def __repr__(self):
        return '{} lps'.format(self.value_lps)

    def __eq__(self, other):
        return self.value_m3ph == other.value_m3ph

    def __lt__(self, other):
        return self.value_m3ph < other.value_m3ph

    def __le__(self, other):
        return self.value_m3ph <= other.value_m3ph

    def __gt__(self, other):
        return self.value_m3ph > other.value_m3ph

    def __ge__(self, other):
        return self.value_m3ph >= other.value_m3ph

    def __add__(self, other):
        self.set(self.value_m3ph + other.value_m3ph, "m3ph")
        return self

    def __mul__(self, other):
        if isinstance(other, FlowVariable):
            raise UnsupportedOperationError("multiply FlowVariables")
        else:
            self.set(self.value_m3ph * other, "m3ph")
            return self

    def __sub__(self, other):
        self.set(self.value_m3ph - other.value_m3ph, "m3ph")
        return self

    def __truediv__(self, other):
        if isinstance(other, FlowVariable):
            raise UnsupportedOperationError("division FlowVariables")
        else:
            self.set(self.value_m3ph / other, "m3ph")
            return self

    def __floordiv__(self, other):
        return self.value_m3ph // other.value_m3ph

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

    def copy(self):
        if self.name is not None:
            self.name += "-copy"
        return FlowVariable(self.value_m3ph, "m3ph", self.name)


class SwitchVariable(Variable):
    """Holds variables which keep switchable things"""

    def __init__(self, value='', dictionary={}):
        super().__init__(value)
        self.dictionary = dictionary


class ResistanceVariable(Variable):
    """Holds list of resistance coefficients"""

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
    """Holds pump characteristic"""

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
        return np.polynomial.polynomial.polyfit(flows, heights, 3)
