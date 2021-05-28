import pompa.models.workpoint
import pompa.models.variables as v
import numpy as np
from pompa.exceptions import WellTooShallowError, WellTooDeepError
from collections import OrderedDict, namedtuple


class PumpSet:

    def __init__(self, station, ord_shutdown, pumps_amount=1):

        # parameters
        self.ORD_STEP = 0.01

        self._well_area = station.well.cr_sec_area()
        self._ord_upper_level = station.hydr_cond.ord_upper_level
        self._req_cycle_time = station.pump_type.cycle_time
        self._ord_inlet = station.hydr_cond.ord_inlet
        self.ins_pipe_area = station.ins_pipe.area()
        self.out_pipe_area = station.out_pipe.area()
        self.pumpset_poly = station.pump_type.characteristic.polynomial_coeff(
            pumps_amount)

        self.min_inflow = station.hydr_cond.inflow_min
        self.max_inflow = station.hydr_cond.inflow_max
        ins_pipe_poly = station.ins_pipe.dynamic_loss_polynomial(
            self.min_inflow, self.max_inflow)
        out_pipe_poly = station.out_pipe.dynamic_loss_polynomial(
            self.min_inflow, self.max_inflow)
        self.pipeset_poly = ins_pipe_poly + out_pipe_poly

        # interface
        self.ord_stop = ord_shutdown
        self.cyc_time = None
        self.wor_time = None
        self.lay_time = None
        self.vol_u = None
        self.ord_start = None
        self.wpoint_start = None
        self.wpoint_stop = None
        self.op_range = None
        self.worst_inflow = None

        # calculations
        self._calculate()

    def _calculate(self):
        Point = namedtuple('Point', ['wpoint', 'it_v', 'it_eff', 'e_time'])
        points = OrderedDict()

        enough_time = False
        ordinate = round(self.ord_stop, 2)

        points[str(ordinate.get())] = Point(
            self._workpoint(ordinate), 0, None, 0)

        while not enough_time:
            ordinate += self.ORD_STEP
            ordinate = round(ordinate, 2)

            if ordinate > self._ord_inlet:
                raise WellTooShallowError

            last_ord = list(points.keys())[-1]

            it_volume = round(
                (ordinate.get() - float(last_ord)) * self._well_area.value, 3)
            wpoint = self._workpoint(ordinate)
            it_avg_eff = (wpoint.flow + points[last_ord].wpoint.flow) / 2
            it_e_time = round(it_volume / it_avg_eff.value_m3ps, 2)

            points[str(ordinate.get())] = Point(
                wpoint, it_volume, it_avg_eff, it_e_time)

            worst_inflow = self._worst_inflow(points)

            c_time, w_time, l_time = self._cycle_times(points, worst_inflow)

            if c_time > self._req_cycle_time.value:
                enough_time = True

        if points[str(self.ord_stop.value)].wpoint.flow > self.max_inflow:
            self.enough_pumps = True

        self.cyc_time = c_time
        self.wor_time = w_time
        self.lay_time = l_time
        self.vol_u = round(
            sum([points[point].it_v for point in points.keys()]), 2)
        self.ord_start = ordinate
        self.wpoint_start = wpoint
        self.wpoint_stop = points[str(self.ord_stop.get())].wpoint
        self.op_range = None
        self.worst_inflow = worst_inflow

        print('c time: ', c_time)
        print('w time: ', w_time)
        print('l time: ', l_time)
        print('vol_u: ', self.vol_u)
        print('wpoint stop: ', self.wpoint_stop)
        print('ord start: ', ordinate)
        print('wpoint start: ', self.wpoint_start)

    def _layover_time(self, points, inflow):
        """ calculates pump layover time, when sewage are filling active volume
        of station
        """
        vol_sum = sum([points[point].it_v for point in points.keys()])
        return round(vol_sum / inflow.value_m3ps, 2)

    def _working_time(self, points, inflow):
        """ Calculates pump working time, considering inflow and real pump
        efficiency on iterative volumes.
        """
        time = 0
        for point in points.values():
            if point.it_eff is None:
                continue
            balance = point.it_eff - inflow
            time += (point.it_v / balance.value_m3ps)
        return round(time, 2)

    def _cycle_times(self, points, inflow):
        """ Calculates pump cycle time as sum of working time and layover time
        points: OrderedDict
            value is namedtuple ['wpoint', 'it_v', 'it_eff', 'e_time']
        worst_inflow: FlowVariable
        """
        working_time = self._working_time(points, inflow)
        layover_time = self._layover_time(points, inflow)
        cycle_time = round(working_time + layover_time, 2)
        return cycle_time, working_time, layover_time

    def _workpoint(self, ordinate):
        return pompa.models.workpoint.WorkPoint(
            self._geom_height(ordinate),
            self.ins_pipe_area, self.out_pipe_area, self.pumpset_poly,
            self.pipeset_poly)

    def _worst_inflow(self, points):
        vol_sum = sum([points[point].it_v for point in points.keys()])
        time_sum = sum([points[point].e_time for point in points.keys()])
        avg_eff = v.FlowVariable(vol_sum / time_sum, 'm3ps')
        return avg_eff / 2

    def _geom_height(self, checked_ord):
        """Returns difference between ordinate of upper well, and current
        ordinate"""
        return self._ord_upper_level - checked_ord
