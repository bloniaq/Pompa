from pompa.models.pumpset import PumpSet
import pompa.models.variables as v
import numpy as np

import matplotlib.pyplot as plt


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

    def _stop_ordinate(self, current_bottom):
        ''' Calculating ordinate where pumps need to stop working.
        Expects FlowVariable as input
        '''
        return v.FloatVariable(current_bottom + self.pump_type.suction_level)

    def _flow_array(self):
        x_min = min(
            self.hydr_cond.inflow_min.value_m3ps - 0.003,
            self.pump_type.efficiency_from.value_m3ps - 0.003)
        x_max = max(
            1.5 * (self.hydr_cond.inflow_max.value_m3ps + 0.003),
            1.5 * (self.pump_type.efficiency_to.value_m3ps + 0.003))
        flow_array = np.linspace(x_min, x_max, 200)
        return flow_array

    def _pipes_dyn_loss_polynomial(self):
        heights = []
        geom_h = 9.32

        for i in self.flow_array:
            ins_h = self.ins_pipe.sum_loss(v.FlowVariable(1000 * i, 'lps'))
            out_h = self.out_pipe.sum_loss(v.FlowVariable(1000 * i, 'lps'))
            print(geom_h, ins_h, out_h)
            heights.append(round(geom_h + ins_h + out_h, 3))

        h = np.array(heights)

        print(heights)

        coeffs = np.polynomial.polynomial.polyfit(self.flow_array, h, 3)

        # MatPlotLib figure to see results

        '''
        poly = np.polynomial.polynomial.Polynomial(coeffs)

        plt.plot(self.flow_array, poly(self.flow_array), 'b-')
        for i in range(len(self.flow_array)):
            plt.plot(self.flow_array[i], heights[i], 'ro')

        plt.show()
        '''

        return coeffs
