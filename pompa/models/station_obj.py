class StationObject():

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
