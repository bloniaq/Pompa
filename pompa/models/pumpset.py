import pompa.models.workpoint
import pompa.models.variables as v
from pompa.exceptions import WellTooShallowError, WellTooDeepError










# PONIŻEJ ZAKOMENTOWANY KOD - PIERWOTNA WERSJA

'''
class PumpSet():

    def __init__(self, required_cycle_time, inflow, pumpset_efficiency,
                 pipeset_poly, pumpset_poly, ins_pipe_area, out_pipe_area,
                 well_area, ord_upper_level, ord_shutdown, ord_inlet,
                 ord_latter_pumpset_startup=None):
        self.required_cycle_time = required_cycle_time
        self.inflow = inflow
        self.pumpset_efficiency = pumpset_efficiency
        self.pipeset_poly = pipeset_poly
        self.pumpset_poly = pumpset_poly
        self.ins_pipe_area = ins_pipe_area
        self.out_pipe_area = out_pipe_area
        self.well_area = well_area
        self.ord_upper_level = ord_upper_level
        self.ord_shutdown = ord_shutdown
        self.ord_inlet = ord_inlet
        if ord_latter_pumpset_startup is not None:
            self.ord_latter_pumpset_startup = ord_latter_pumpset_startup
        else:
            self.ord_latter_pumpset_startup = ord_shutdown

        self.workpoints = []
        self.efficiencys = []
        self.cycle_time = 0
        self.working_time = 0
        self.layover_time = 0

        self.h_iterator = 0.01

    def calculate(self):
        print('\nworkpoint bottom')
        self.workpoints.append(self._workpoint(self.ord_shutdown.value))

        enough_time = False
        current_ordinate = self.ord_shutdown

        while not enough_time:
            print('\nworkpoint number ', len(self.workpoints))
            current_ordinate.set(current_ordinate.value + self.h_iterator)
            print('curr ord', current_ordinate)
            if current_ordinate >= self.ord_inlet:
                raise WellTooShallowError
                break

            self.workpoints.append(self._workpoint(current_ordinate))
            self.efficiencys.append(self._current_average_eff())
            self.worst_inflow = self._worst_inflow(
                self._absolute_average_eff())
            print('current worst ', self.worst_inflow)

            self._update_cycle_times(self._absolute_average_eff())

            if self.cycle_time >= self.required_cycle_time:
                print('enough_time')
                enough_time = True

        if self.ord_inlet - current_ordinate > 0.3:
            # raise WellTooDeepError
            pass

        result = {}
        result['working_time'] = round(self.working_time)
        result['layover_time'] = round(self.layover_time)
        result['cycle_time'] = result['working_time'] + result['layover_time']
        result['useful_velo'] = self._useful_velo(current_ordinate)
        result['start_ordinate'] = current_ordinate
        result['stop_wpoint'] = self.workpoints[0]
        result['start_wpoint'] = self.workpoints[-1]
        result['efficiency_from'] = self.pumpset_efficiency[0]
        result['efficiency_to'] = self.pumpset_efficiency[1]
        result['worst_inflow'] = self.worst_inflow

        return result

    def _workpoint(self, ordinate):
        workpoint = pompa.models.workpoint.WorkPoint(
            self._geom_height(ordinate), self.ins_pipe_area,
            self.out_pipe_area, self.pumpset_poly, self.pipeset_poly)
        return workpoint.calculate()

    def _worst_inflow(self, average_efficiency):
        """Returns the worst inflow in case of pumpset. It is equal to half
        of outflow value. Expects average_efficiency as FlowVariable.
        Retruns FlowVariable"""
        absolute_worst_inflow = average_efficiency / 2
        if self.inflow[0] <= absolute_worst_inflow <= self.inflow[1]:
            worst_inflow = absolute_worst_inflow
        elif absolute_worst_inflow < self.inflow[0]:
            worst_inflow = self.inflow[0]
        elif self.inflow[1] < absolute_worst_inflow:
            worst_inflow = self.inflow[1]
        return worst_inflow

    def _geom_height(self, checked_ord):
        """Returns difference between ordinate of upper well, and current
        ordinate"""
        return self.ord_upper_level - checked_ord

    def _velocity(self, checked_height):
        """Returns value of well velocity in passed height, based on well
        cross-sectional area"""
        return round(self.well_area * checked_height, 2)

    def _current_average_eff(self):
        """Returns FlowVariable type event to average flow of last two
        workpoints in self.workpoints list"""
        last_eff = self.workpoints[-1]['flow']
        last_but_one_eff = self.workpoints[-2]['flow']
        return (last_eff + last_but_one_eff) / 2

    def _absolute_average_eff(self):
        """Returns FlowVariable-typed value of average efficiency of pumping"""
        return sum(self.efficiencys, v.FlowVariable(0)) / len(self.efficiencys)

    def _update_cycle_times(self, avg_flow):
        iterator_velo = self._velocity(self.h_iterator)
        layover_time_addition = iterator_velo / self.worst_inflow.value_m3ps
        working_time_addition = iterator_velo / (
            avg_flow - self.worst_inflow).value_m3ps
        self.layover_time += layover_time_addition
        self.working_time += working_time_addition
        self.cycle_time = self.working_time + self.layover_time
        pass

    def _useful_velo(self, start_ordinate):
        """Returns useful velocity of pumpset. Expects FloatVariable as
        start_ordinate argument."""
        height = start_ordinate - self.ord_latter_pumpset_startup
        return self._velocity(height.value)

'''
