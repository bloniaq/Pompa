# libraries
import logging

log = logging.getLogger('pompa.models')


class StationObject():

    kinematic_viscosity = 1.0068  # [mm²/s] dla 20°C
    std_grav = 9.81

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.ui_vars = app.builder.tkvariables

    def __setattr__(self, attr, value):
        if '.' not in attr:
            self.__dict__[attr] = value
        else:
            attr_name, rest = attr.split('.', 1)
            setattr(getattr(self, attr_name), rest, value)

    def __getattr__(self, attr):
        if '.' not in attr:
            log.debug('{} Has no <.> in attr'.format(self))
            return super().__getattr__(attr)
        else:
            attr_name, rest = attr.split('.', 1)
            return getattr(getattr(self, attr_name), rest)

    def load_data(self, data_dict):
        for attribute in self.__dict__:
            log.debug('loading {} for obj {}'.format(attribute, self))
            if hasattr(self.__dict__[attribute], 'dan_id'):
                log.debug('{} has dan_id'.format(attribute))
                self.__dict__[attribute].load_data(data_dict)
