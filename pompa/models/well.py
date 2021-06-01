import pompa.models.variables as v


class Well(v.StationObject):

    def __init__(self):
        """
        shape: round, rectangle - shape of well
        config: optimal, singlerow - strings defining pump configuration
        diameter: [meters]
        length:
        width:
        """
        self.shape = v.SwitchVariable()
        self.config = v.SwitchVariable()
        self.diameter = v.FloatVariable()
        self.length = v.FloatVariable()
        self.width = v.FloatVariable()

    def minimal_diameter(self, n_of_pumps, netto_contour):
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

        if self.config == 'optimal':
            min_diam = patterns[str(n_of_pumps)](contour)
        elif self.config == 'singlerow':
            min_diam = n_of_pumps * contour

        min_diam = round(min_diam, 2)

        return min_diam

    def cr_sec_area(self):
        if self.shape.value == 'rectangle':
            return v.FloatVariable(round(
                self.width.value * self.length.value, 2))
        elif self.shape.value == 'round':
            return v.FloatVariable(round(pow(
                self.diameter.value / 2, 2) * 3.14, 2))
