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
        self.min_length = 0
        self.min_width = 0

    def update(self):
        self.area = round(self.cross_sectional_area(), 2)

    def minimal_diameter(self, n_of_pumps, countour, config):
        """ Returns minimal diameter of round-shaped well.
        Based on number of pumps and contour of single pump
        """
        log.debug('shape: {}'.format(self.shape))
        log.debug('shape type: {}'.format(type(self.shape)))
        if config == 'optimal':
            min_diam = countour + 0.6 + 2 * \
                ((countour + 0.6) / (2 * (np.sin(3.14 / n_of_pumps))))
        elif config == 'singlerow':
            min_diam = (n_of_pumps * countour) + 0.6
        return min_diam

    def minimal_rect_dims(self, n_of_pumps, countour, config):
        """ Returns minimal dimensions of rectangle-shaped well.
        Based on number of pumps and contour of single pump
        """
        if config == 'optimal':
            length, width = self.length.value, self.width.value
            short_side = min(length, width)
            rows = short_side // (countour + 0.6)
            if n_of_pumps % rows == 0:
                pumps_in_row = n_of_pumps / rows
            else:
                pumps_in_row = (n_of_pumps // rows) + 1
            min_len = pumps_in_row * (countour + 0.6)
            min_wid = rows * (countour + 0.6)
        elif config == 'singlerow':
            min_len = n_of_pumps * (countour + 0.6)
            min_wid = countour + 0.6
        return min_len, min_wid

    def update_min_dimensions(self, shape, config):
        """ Calculates values of proper min dimensions parameters.
        Checks shape and runs proper function which returns values.
        """
        validation_flag = True
        if shape == 'round':
            self.min_diameter = self.minimal_diameter(
                self.station.n_of_pumps + self.station.n_of_res_pumps,
                self.station.pump.countour, config)
            if not self.min_diameter:
                validation_flag = False
        elif shape == 'rectangle':
            self.min_length, self.min_width = self.minimal_rect_dims(
                self.station.n_of_pumps + self.station.n_of_res_pumps,
                self.station.pump.countour, config)
            if not (self.min_length and self.min_width):
                validation_flag = False
        return validation_flag

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
