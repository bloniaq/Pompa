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

        # input parameters
        self.shape = None
        self.config = None
        self.diameter = 0
        self.length = 0
        self.width = 0

        # parameters to calculate
        self.area = 0
        self.min_diameter = 0
        self.diameter_fung = 0

    def update(self):
        self.area = round(self.cross_sectional_area(), 2)

    def minimal_diameter(self, n, station):
        d = station.pump.contour.value
        log.debug('shape: {}'.format(self.shape))
        log.debug('shape type: {}'.format(type(self.shape)))
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
            self.diameter_fung = round(2 * ((area / 3.14) ** 0.5), 2)
        elif self.shape.value == 'round':
            log.debug('round')
            log.debug('diameter value: {}'.format(self.diameter.value))
            area = 3.14 * ((self.diameter.value / 2) ** 2)
            self.diameter_fung = self.diameter.value
        log.debug('cross section area is {}'.format(area))
        return area
