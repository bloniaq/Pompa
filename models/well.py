# libraries
import logging
import numpy as np

# modules
import models.models as models

log = logging.getLogger('pompa.well')


class Well(models.StationObject):
    """class for well"""

    def __init__(self, app):
        super().__init__(app)

        self.pump_type = None
        self.discharge_pipe = None
        self.collector = None

        self.reserve_pumps = None
        self.shape = None
        self.config = None
        # self.set_shape(self.default['shape'])
        self.diameter = 0
        self.length = 0
        self.width = 0

    def set_shape(self, shape):
        self.ui_vars.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = self.builder.get_object('Entry_Well_diameter')
        length = self.builder.get_object('Entry_Well_length')
        width = self.builder.get_object('Entry_Well_width')
        if shape == 'round':
            diameter.configure(state='normal')
            length.configure(state='disabled')
            width.configure(state='disabled')
        elif shape == 'rectangle':
            diameter.configure(state='disabled')
            length.configure(state='normal')
            width.configure(state='normal')
        log.debug('changed shape to {}'.format(shape))

    def minimal_diameter(self, n_work_pumps, n_reserve_pumps, station):
        d = station.pump_type.contour.value
        n = n_work_pumps + n_reserve_pumps
        if self.shape.value == 'round':
            if self.config.value == 'optimal':
                minimal_d = d + 0.6 + 2 * \
                    ((d + 0.6) / (2 * (np.sin(3.14 / n))))
            elif self.config.value == 'singlerow':
                minimal_d = (n * d) + 0.6
        elif self.shape.value == 'rectangle':
            if self.config.value == 'optimal':
                length, width = self.length.value, self.width.value
                short_side = min(length, width)
                rows = short_side // (d + 0.6)
                if n % rows == 0:
                    pumps_in_row = n / rows
                else:
                    pumps_in_row = (n // rows) + 1
                min_len = pumps_in_row * (d + 0.6)
                min_wid = rows * (d + 0.6)
            elif self.config.value == 'singlerow':
                min_len = n * (d + 0.6)
                min_wid = d + 0.6
            minimal_d = 2 * ((min_len * min_wid / 3.14) ** (1 / 2))
        return minimal_d

    def cross_sectional_area(self):
        if self.shape.value == 'rectangle':
            log.debug('rectangle')
            area = self.length.value * self.width.value
            log.debug('len: {}, wid: {}'.format(
                self.length.value, self.width.value))
        elif self.shape.value == 'round':
            log.debug('round')
            log.debug('diameter value: {}'.format(self.diameter.value))
            area = 3.14 * ((self.diameter.value / 2) ** 2)
        log.debug('cross section area is {}'.format(area))
        return area
