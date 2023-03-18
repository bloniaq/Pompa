from pompa.models.pumpset import PumpSet
import math


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

        self.station = station
        self.enough_pumps = False
        self.pumpsets = []
        self.reserve_pumps = 0
        self.all_pumps = 0
        self._ord_shutdown = station.pump_type.shutdown_ord

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
        ord_bottom = self.station.hydr_cond.ord_bottom
        pumps_counter = 0

        while not enough_pumps:
            pumps_counter += 1
            if len(self.pumpsets) == 0:
                last_pset = None
            else:
                last_pset = self.pumpsets[-1]
            self.pumpsets.append(PumpSet(self.station, self._ord_shutdown(
                ord_bottom), pumps_counter, last_pset))
            print('pumpsets len: ', len(self.pumpsets))
            enough_pumps = self.pumpsets[-1].enough_pumps
            if pumps_counter == PUMPSETS_LIMITER:
                enough_pumps = True

        self.reserve_pumps = self._calc_reserve_pumps(pumps_counter)

    def _calc_reserve_pumps(self, working_pumps: int):
        mode = self.station.safety.value
        print(mode)
        if mode == 'economic':
            return 1
        elif mode == 'optimal':
            return math.ceil(working_pumps / 2)
        elif mode == 'safe':
            return working_pumps

    def _update_all_pumps_number(self):
        self.all_pumps = len(self.pumpsets) + self.reserve_pumps
