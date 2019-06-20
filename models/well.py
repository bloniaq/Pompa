# libraries
import logging
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

    def minimal_diameter(self, n_of_pumps, netto_contour, config):
        """ Returns minimal diameter of round-shaped well.
        Based on number of pumps and contour of single pump
        """
        contour = netto_contour + 0.3

        patterns = {'1': (lambda d: d),
                    '2': (lambda d: 2 * d),
                    '3': (lambda d: 2.16 * d),
                    '4': (lambda d: 2.42 * d),
                    '5': (lambda d: 2.70 * d),
                    '6': (lambda d: 3 * d),
                    '7': (lambda d: 3 * d),
                    '8': (lambda d: 3.30 * d),
                    '9': (lambda d: 3.61 * d),
                    '10': (lambda d: 3.81 * d),
                    '11': (lambda d: 3.92 * d),
                    '12': (lambda d: 4.03 * d),
                    '13': (lambda d: 4.24 * d),
                    '14': (lambda d: 4.33 * d),
                    '15': (lambda d: 4.52 * d),
                    '16': (lambda d: 4.62 * d),
                    '17': (lambda d: 4.79 * d),
                    '18': (lambda d: 4.86 * d),
                    '19': (lambda d: 4.86 * d),
                    '20': (lambda d: 5.12 * d)}

        log.debug('shape: {}'.format(self.shape))
        log.debug('shape type: {}'.format(type(self.shape)))
        if config == 'optimal':
            min_diam = patterns[str(n_of_pumps)](contour)
        elif config == 'singlerow':
            min_diam = n_of_pumps * contour
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
        statement = ''
        if shape == 'round':
            self.min_diameter = self.minimal_diameter(
                sum_pumps, pump_contour, config)
            if not self.min_diameter:
                statement = '\nNie obliczono minimalnej średnicy'
            if self.min_diameter > self.diameter.value:
                statement = '\nUWAGA! Dobrano liczbę pomp przekraczającą ' + \
                    'możliwości montażowe studni'
        elif shape == 'rectangle':
            self.min_length, self.min_width = self.minimal_rect_dims(
                sum_pumps, pump_contour, config)
            if not (self.min_length and self.min_width):
                statement = '\nNie obliczono minimalnych wymiarów'
            if (self.min_width > self.width.value or
                    self.min_length > self.length.value):
                statement = '\nUWAGA! Dobrano liczbę pomp przekraczającą ' + \
                    'możliwości montażowe studni'
        if statement != '':
            statement += '\n\n'
        return statement

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
