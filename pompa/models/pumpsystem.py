from pompa.models.pumpset import PumpSet


PUMPSETS_LIMITER = 5


class PumpSystem:
    """Class used to keep Pumpsystem - all pumps in the station - calculations.

    Attributes
    ----------
    pumpsets : list
        List of pumpsets calculated iteratively until requirement of efficiency
        is fulfilled
    """

    def __init__(self, station, mode='checking'):
        """
        Parameters
        ----------
        station : Station
            The sewage pump station
        mode : str
            User-chosen mode of pumpsystem calculation (default = 'checking')
        """

        self._station = station
        self.pumpsets = []

        self._calculate(mode)

    def _calculate(self, mode):
        """Made calculations based on chosen mode"""

        pick_method = {'checking': self._checking_mode}
        pick_method[mode]()

    def _checking_mode(self):
        """Calculate whether assumed bottom ordinate will let pump have
        appropriate cycle time in condition of least favorable inflow.
        """

        self.pumpsets = []
        enough_pumps = False
        ord_bottom = self._station.hydr_cond.ord_bottom
        pumps_counter = 0

        while not enough_pumps:
            pumps_counter += 1
            if len(self.pumpsets) == 0:
                last_pset = None
            else:
                last_pset = self.pumpsets[-1]
            self.pumpsets.append(PumpSet(self._station, self._ord_shutdown(
                ord_bottom), pumps_counter, last_pset))
            print('pumpsets len: ', len(self.pumpsets))
            enough_pumps = self.pumpsets[-1].enough_pumps
            if pumps_counter == PUMPSETS_LIMITER:
                enough_pumps = True

    def _ord_shutdown(self, ord_bottom):
        """Calculate ordinate of pump shutdown.

        Parameters
        ----------
        ord_bottom : FloatVariable
            Current station bottom ordinate

        Returns
        -------
        FloatVariable
            Sum of current bottom ordinate and pumptype suction level.
        """

        return self._station.pump_type.suction_level + ord_bottom
