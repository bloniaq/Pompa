from pompa.models.pumpset import PumpSet
import pompa.models.variables as v
import numpy as np

import matplotlib.pyplot as plt


PUMPSET_LIMITER = 5


class PumpSystem:

    def __init__(self, station, mode='checking'):
        self.station = station
        self.mode = mode
        self.pumpsets = []

        self._calculate(mode)

    def _calculate(self, mode):
        """ Picks method of calculations based on mode chosen by user
        """
        pick_method = {'checking': self._checking_mode}
        pick_method[mode]()

    def _checking_mode(self):
        """ Checks whether assumed bottom ordinate will let pump have
        appropriate cycle time in worst inflow condition.
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
            if pumps_counter == PUMPSET_LIMITER:
                enough_pumps = True

    def _ord_shutdown(self, ord_bottom):
        """ Calculates ordinate of pumo shutdown as a sum of current bottom
        ordinate and pumptype suction level.
        """
        return self.station.pump_type.suction_level + ord_bottom
