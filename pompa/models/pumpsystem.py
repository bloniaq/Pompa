from pompa.models.pumpset import PumpSet
import pompa.models.variables as v
import numpy as np

import matplotlib.pyplot as plt


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
        enough_pumps = False
        ord_bottom = self.station.hydr_cond.ord_bottom

        while not enough_pumps:
            self.pumpsets.append(PumpSet(self.station, self._ord_shutdown(
                ord_bottom)))
            enough_pumps = True

    def _ord_shutdown(self, ord_bottom):
        """ Calculates ordinate of pumo shutdown as a sum of current bottom
        ordinate and pumptype suction level.
        """
        return self.station.pump_type.suction_level + ord_bottom


# KOD ZAKOMENTOWANY
# DO WYRZUCENIA PO URUCHOMIENIU WERSJI NA CZYSTO (POWYZEJ)

"""
class PumpSystem():
    '''
    '''

    def __init__(self, well, ins_pipe, out_pipe, pump_type,
                 hydr_cond, mode='checking'):
        self.well = well
        self.ins_pipe = ins_pipe
        self.out_pipe = out_pipe
        self.pump_type = pump_type
        self.hydr_cond = hydr_cond
        self.mode = mode

        self.flow_array = self._flow_array()

        self.pumpsets = []

    def checking(self):
        counter = 1
        enough_pumps = False
        '''
        while not enough_pumps:
            self.pumpsets.append(PumpSet(
                self.pump_type,
                self._stop_ordinate(self.hydr_cond.ord_bottom),
                counter,
                self.hydr_cond.inflow_min,
                self.hydr_cond.inflow_max))
            if counter == 3:
                enough_pumps = True
            counter += 1
        '''
        self.pumpsets = [1, 1, 1]

    def _stop_ordinate(self, current_bottom):
        ''' Calculating ordinate where pumps need to stop working.
        Expects FlowVariable as input
        '''
        return current_bottom + self.pump_type.suction_level

    def _flow_array(self):
        x_min = min(
            self.hydr_cond.inflow_min.value_m3ps - 0.003,
            self.pump_type.efficiency_from.value_m3ps - 0.003)
        x_max = max(
            1.5 * (self.hydr_cond.inflow_max.value_m3ps + 0.003),
            1.5 * (self.pump_type.efficiency_to.value_m3ps + 0.003))
        flow_array = np.linspace(x_min, x_max, 200)
        return flow_array
"""
