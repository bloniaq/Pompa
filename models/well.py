# libraries
import logging
import numpy as np
import math

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

    def minimal_rect_dims(self, n_of_pumps, netto_contour, config):
        """ Returns minimal dimensions of rectangle-shaped well.
        Based on number of pumps and contour of single pump
        """
        contour = netto_contour + 0.6

        patterns = {'1': (lambda d: d),
                    '2': (lambda d: (2 + (2 ** (0.5)) / (2 * d))),
                    '3': (lambda d: (
                        4 + (2 ** (0.5)) + (6 ** (0.5))) / (4 * d)),
                    '4': (lambda d: 2 * d),
                    '5': (lambda d: d / ((2 ** 0.5) - 1))}

        def more_pumps(n_of_pumps, contour):
            current_wid = self.width.value
            if current_wid / contour <= 2.5:
                # RAISE SOME EXCEPTION !!!
                dim1 = 1.5 * contour
                dim2 = n_of_pumps * ((contour / 2) * (3 ** 0.5))
            elif current_wid / contour <= 3.5:
                dim1 = 2.5 * contour
                dim2 = math.ceil(n_of_pumps / 2) * contour * (3 ** 0.5)
            elif current_wid / contour > 3.5:
                dim1 = 3.5 * contour
                dim2 = math.ceil(n_of_pumps / 3) * contour * (3 ** 0.5)
            min_wid = min(dim1, dim2)
            min_len = max(dim1, dim2)

            return min_len, min_wid

        if config == 'optimal':
            if n_of_pumps > 5:
                min_len, min_wid = more_pumps(n_of_pumps, contour)
            else:
                min_len = min_wid = patterns[str(n_of_pumps)](contour)

        elif config == 'singlerow':
            min_len = n_of_pumps * contour
            min_wid = contour
        return min_len, min_wid

    def update_min_dimensions(self, shape, sum_pumps, pump_contour, config):
        """ Calculates values of proper min dimensions parameters.
        Checks shape and runs proper function which returns values.
        """
        validation_flag = True
        if shape == 'round':
            self.min_diameter = self.minimal_diameter(
                sum_pumps, pump_contour, config)
            if not self.min_diameter:
                validation_flag = False
        elif shape == 'rectangle':
            self.min_length, self.min_width = self.minimal_rect_dims(
                sum_pumps, pump_contour, config)
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
