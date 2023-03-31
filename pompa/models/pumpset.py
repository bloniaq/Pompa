import pompa.models.workpoint
import pompa.models.variables as v
from pompa.exceptions import WellTooShallowError, WellTooDeepError
from collections import OrderedDict, namedtuple


class PumpSet:
    """Class used to represent a Pumpset.

    Pumpset is a specific configuration of installed in station pumps, has a
    specific ordinate of shutdown, specific ordinate of start-up, which have to
    fulfill criteria of minimum cycle time provided by pump manufacturer.

    Attributes
    ----------
    ord_stop : FloatVariable
        The ordinate of pumpset shutdown
    cyc_time : float
        Time of cycle, sum of working- and layover time
    wor_time : float
        Time of working, based on balance between inflow and pump efficiency
    lay_time : float
        Time of layover - time when inflow fulfill useful volume of station
    vol_u : float
        Useful volume of station, volume between start- and stop ordinate
    ord_start : FloatVariable
        The ordinate of pumpset start-up
    wpoint_start : WorkPoint
        Workpoint parameters at start-up ordinate
    wpoint_stop : WorkPoint
        Workpoint parameters at shutdown ordinate
    opt_range : tuple
        Optimal range of pumpset efficiency. (min, max)
    worst_inflow : FlowVariable
        The least favorable inflow
    enough_pumps : bool
        Is true, when pumpset efficiency at shutdown ordinate (lowest eff) is
        higher than maximum expected inflow

    TODO: Private attributes description
    """

    def __init__(self, station, ord_shutdown, pumps_amount=1, last_pset=None):
        """
        Calculates the necessary parameters, then calculates the main params
        of pumpset.

        Parameters
        ----------
        station : Station
            The sewage station
        ord_shutdown : FloatVariable
            The assumed ordinate of pumpset shutdown
        pumps_amount : int, optional
            Number of pumps working in pumpset (default is 1)
        last_pset : PumpSet, optional
            The set of pumps smaller by one pump
        """

        # parameters
        self._ORD_STEP = 0.01

        self.pumps_amount = pumps_amount
        self.station = station
        self._out_pipes_no = station.out_pipes_no.get()
        self._well_area = station.well.cr_sec_area()
        self._ord_upper_level = station.hydr_cond.ord_upper_level
        self._req_cycle_time = station.pump_type.cycle_time.value * 60
        self._max_inlet_ordinate = station.hydr_cond.ord_inlet - station.hydr_cond.reserve_height
        self._ins_pipe_area = station.ins_pipe.area()
        self._out_pipe_area = station.out_pipe.area()
        self.pumpset_poly = station.pump_type.characteristic.polynomial_coeff(
            pumps_amount, self.station.fixing_mode)
        self._geom_height = station.hydr_cond.geom_height

        if last_pset is None:
            self.last_pset_start_ord = ord_shutdown
        else:
            self.last_pset_start_ord = last_pset.ord_start
        if pumps_amount == 1:
            last_pset_start_q = v.FlowVariable(0)
            """
            Te zakomentowane linijki to stare rozwiazanie, które powodowało że 
            próba wykonania powtórnych obliczeń była blokowana z powodu powołania
            zmienny o zajętej już nazwie. Problem unikalności zmiennych w modelu
            należałoby jakoś w przyszłości rozwiązać
            """
            # self._min_ord = ord_shutdown.copy(f"min_ord_pump_{pumps_amount}")
            self._min_ord = ord_shutdown.get()
        elif pumps_amount > 1:
            last_pset_start_q = last_pset.wpoint_start.flow.copy()
            # self._min_ord = last_pset.ord_start.copy(
            #     f"min_ord_pump_{pumps_amount}")

            # pompa 1.0 przynajmniej w trybie checking podaje tę samą rzędną
            # włączenia dla kolejnych włączanych pomp
            self._min_ord = last_pset.ord_start.get() + 0.1

        self.min_inflow = max(station.hydr_cond.inflow_min,
                              v.FlowVariable(.1, 'lps') + last_pset_start_q)
        self.max_inflow = station.hydr_cond.inflow_max
        ins_pipe_poly = station.ins_pipe.dynamic_loss_polynomial(
            self.min_inflow, self.max_inflow, pumps_amount)
        out_pipe_poly = station.out_pipe.dynamic_loss_polynomial(
            self.min_inflow, self.max_inflow, self._out_pipes_no)
        self.pipeset_poly = ins_pipe_poly + out_pipe_poly

        # interface
        self.enough_pumps = False

        self.ord_stop = ord_shutdown.copy()
        self.cyc_time = None
        self.wor_time = None
        self.lay_time = None
        self.vol_u = None
        self.ord_start = None
        self.wpoint_start = None
        self.wpoint_stop = None
        self.opt_range = station.pump_type.opt_range(pumps_amount)
        self.worst_inflow = None

        # calculations
        self._calculate()

    def _calculate(self):
        """Calculate main pumpset parameters.

        First calculates workpoint at shutdown ordinate. Then it goes into
        loop, and calculates workpoints at incrementing ordinates, until it
        finds ordinate, which let pass requirements of cycle time.

        Raises
        ------
        WellTooShallowError
            If ordinate which fulfill requirements is higher than inlet
            ordinate
        WellTooDeepError (NOT IMPLEMENTED YET)
            If ordinate which fulfill requirements is significantly lower
            than inlet ordinate
        """

        Point = namedtuple('Point', ['wpoint', 'it_v', 'it_eff', 'e_time'])
        points = OrderedDict()

        enough_time = False
        ordinate = v.FloatVariable(self.ord_stop.value, digits=2)
        points[str(ordinate.get())] = Point(
            self._workpoint(ordinate), 0, None, 0)

        c_time = 0

        while not enough_time:
            ordinate += self._ORD_STEP
            ordinate = round(ordinate, 2)

            last_ord = list(points.keys())[-1]

            if ordinate > self._max_inlet_ordinate:
                raise WellTooShallowError(ordinate, self._max_inlet_ordinate,
                                          c_time, self.pumps_amount)

            it_volume = round(
                (ordinate.get() - float(last_ord)) * self._well_area.value, 3)
            wpoint = self._workpoint(ordinate)

            # it_avg_eff = (wpoint.flow + points[last_ord].wpoint.flow) / 2
            it_avg_eff = self._average_flow(
                wpoint.flow, points[last_ord].wpoint.flow)

            it_e_time = round(it_volume / it_avg_eff.value_m3ps, 2)

            points[str(ordinate.get())] = Point(
                wpoint, it_volume, it_avg_eff, it_e_time)

            worst_inflow = self._worst_inflow(points)

            c_time, w_time, l_time = self._cycle_times(points, worst_inflow)

            if (c_time >= self._req_cycle_time and
                    ordinate >= self._min_ord):
                enough_time = True

        if points[str(self.ord_stop.value)].wpoint.flow > self.max_inflow:
            self.enough_pumps = True

        # TODO: WellTooDeepError implementation

        self.cyc_time = round(c_time, 1)
        self.wor_time = round(w_time, 1)
        self.lay_time = round(l_time, 1)
        self.vol_u = round(self.station.well.cr_sec_area().get() * (
                ordinate.get() - self.last_pset_start_ord.get()), 2)
        # self.vol_u = round(
        #     sum([points[point].it_v for point in points.keys()]), 2)
        self.ord_start = ordinate
        self.wpoint_start = wpoint
        self.wpoint_stop = points[str(self.ord_stop.get())].wpoint
        self.worst_inflow = worst_inflow

        print('\n\nPUMP no {}\n'.format(self.pumps_amount))
        print('c time: ', c_time)
        print('w time: ', w_time)
        print('l time: ', l_time)
        print('vol_u: ', self.vol_u)
        print('wpoint stop: ', self.wpoint_stop)
        print('ord start: ', ordinate)
        print('wpoint start: ', self.wpoint_start)
        print('worst_inflow: {}\n\n'.format(worst_inflow))

    def _layover_time(self, points, inflow):
        """Calculate pump layover time.

        Layover time is time when inflow sewage fill the current useful volume

        Parameters
        ----------
        points : OrderedDict
            The discrete data on previous calculations of ordinates workpoints
        inflow : FlowVariable
            The least favorable inflow
        """

        vol_sum = sum([points[point].it_v for point in points.keys()])
        return round(vol_sum / inflow.value_m3ps, 2)

    def _working_time(self, points, inflow):
        """Calculate pump working time.

        Working time is time when pumpset pump out the current useful volume
        during continous inflow

        Parameters
        ----------
        points : OrderedDict
            The discrete data on previous calculations of ordinates workpoints
        inflow : FlowVariable
            The least favorable inflow
        """

        time = 0
        for point in points.values():
            # TODO: Is not None
            if point.it_eff is None:
                continue
            balance_m3ps = point.it_eff.value_m3ps - inflow.value_m3ps
            # balance = point.it_eff - inflow
            balance = v.FlowVariable(balance_m3ps, "m3ps")
            time += (point.it_v / balance.value_m3ps)
        return round(time, 2)

    def _cycle_times(self, points, inflow):
        """Calculate pumpset cycle time.

        Cycle time is a sum of working time and layover time.

        Parameters
        ----------
        points : OrderedDict
            The discrete data on previous calculations of ordinates workpoints
        inflow : FlowVariable
            The least favorable inflow

        Returns
        -------
        tuple
            A tuple of cycle time, working time and layover time
        """

        working_time = self._working_time(points, inflow)
        layover_time = self._layover_time(points, inflow)
        cycle_time = round(working_time + layover_time, 2)
        return cycle_time, working_time, layover_time

    def _workpoint(self, ordinate):
        """Return workpoint parameters at asked ordinate.

        Parameters
        ----------
        ordinate : FloatVariable
            ordinate to calculate its workpoint

        Returns
        -------
        WorkPoint
            object is list of work point parameters.
        """

        return pompa.models.workpoint.WorkPoint(
            self._geom_height(ordinate),
            self._ins_pipe_area, self._out_pipe_area, self.pumpset_poly,
            self.pipeset_poly, self.pumps_amount, self._out_pipes_no)

    def _worst_inflow(self, points):
        """Calculate least favorable inflow.

        Least favorable inflow is basically half of pumpset efficiency.
        Although worst inflow for pumpset can't be lower than efficiency of
        smaller pumpset, and have to be in the range of station minimum and
        maximum inflow.

        Parameters
        ----------
        points : OrderedDict
            The discrete data on previous calculations of ordinates workpoints
        """

        vol_sum = sum([points[point].it_v for point in points.keys()])
        time_sum = sum([points[point].e_time for point in points.keys()])
        avg_eff = v.FlowVariable(vol_sum / time_sum, 'm3ps')
        worst_inflow = min(max(
            avg_eff / 2, self.min_inflow), self.max_inflow)
        return worst_inflow

    def _average_flow(self, flow_1, flow_2, name=None):
        average = (flow_1.value_m3ph + flow_2.value_m3ph) / 2
        return v.FlowVariable(average, "m3ph", name=name)
