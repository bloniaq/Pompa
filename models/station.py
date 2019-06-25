# libraries
import logging
# import math

# modules
import models.models as models
import models.variables as v
import calculation as calc

log = logging.getLogger('pompa.station')


class Station(models.StationObject):

    def __init__(self, app):
        super().__init__(app)

        # components
        self.well = None
        self.ins_pipe = None
        self.out_pipe = None
        self.pump = None
        self.ground = None

        # input parameters
        self.minimal_sewage_level = None
        self.ord_terrain = None
        self.ord_inlet = None
        self.ord_outlet = None
        self.ord_bottom = None
        self.difference_in_start = None
        self.ord_highest_point = None
        self.ord_upper_level = None
        self.inflow_max = None
        self.inflow_min = None

        # parameters to update
        self.min_sew_ord = None
        self.area = None

        # parameters to calculate
        self.work_parameters = None
        self.n_of_pumps = 0
        self.n_of_res_pumps = 0
        self.statement = ''

    def update(self):
        self.well.update()
        self.pump.update()
        self.ins_pipe.update()
        self.out_pipe.update()

    def height_to_pump(self, lower_ord):
        height = self.ord_upper_level.value - lower_ord
        return height

    def minimal_sewage_ord(self, ord_bottom):
        return ord_bottom + self.minimal_sewage_level.value

    def average_flow(self, flow1, flow2):
        average_value = (flow1.v_lps + flow2.v_lps) / 2
        av_inflow = v.CalcFlow(average_value, unit="liters")
        return av_inflow

    def pipes_ready(self):
        """returns if there both pipe has data to draw figures
        """
        log.debug('Are pipes ready?')
        flag = True
        if not self.ins_pipe.pipe_char_ready():
            flag = False
        log.debug(flag)
        if not self.out_pipe.pipe_char_ready():
            flag = False
        log.debug(flag)
        return flag

    def geom_loss_ready(self):
        log.debug('Are pipes ready?')
        flag = True
        checklist = [self.ord_bottom, self.minimal_sewage_level]
        for parameter in checklist:
            if parameter is None:
                flag = False
                return flag
        for parameter in checklist:
            log.debug('{} = {}'.format(parameter, parameter.value))
            if parameter.value == 0:
                flag = False
        return flag

    def velocity(self, height):
        velocity = self.well.area * height
        log.debug('v for h: {} is {}'.format(height, velocity))
        return velocity

    def calculate(self, mode):
        """ Returns validation flag

        Runs calculations and checks if results exists and if are correct.
        """
        self.update()
        self.statement = ''
        validation_flag = True

        calculations = {'minimalisation': self.calc_minimalisation,
                        'checking': self.calc_checking,
                        'optimalisation': self.calc_optimalisation}
        log.debug('mode: {}'.format(mode))
        log.debug('type dict val: {}'.format(type(calculations[mode])))

        validation_flag = calculations[mode]()

        self.n_of_res_pumps = self.reserve_pumps_number(
            self.reserve_pumps.value, self.n_of_pumps)
        self.statement += self.well.update_min_dimensions(
            self.well.shape.value,
            self.n_of_pumps + self.n_of_res_pumps,
            self.pump.contour.value,
            self.well.config.value)

        self.h_whole = self.ord_terrain.value - self.ord_bottom.value
        self.v_whole = self.velocity(self.h_whole)
        self.h_useful = self.work_parameters[str(
            self.n_of_pumps)]['ord_sw_on'] - self.ord_sw_off
        self.v_useful = self.velocity(self.h_useful)

        self.ord_sw_on = self.work_parameters[str(
            self.n_of_pumps)]['ord_sw_on']
        self.ord_sw_alarm = self.ord_inlet.value
        self.h_reserve = round(self.ord_sw_alarm - self.ord_sw_on, 2)
        if self.h_reserve < 0:
            self.statement += '\nUWAGA! Rzędna włączenia pomp powyżej dna ' + \
                'przewodu doprowadzającego ścieki do pompowni\n\n'
        self.v_reserve = self.velocity(self.h_reserve)

        self.v_dead = self.velocity(self.minimal_sewage_level.value)

        if mode == 'minimalisation':
            well_height = self.ord_terrain.value - self.ord_bottom.value
            self.ground.parameters(self.out_pipe, self.well, well_height)

        return validation_flag

    def calc_minimalisation(self):

        log.error('CALC_MINIMALISATION')
        validation_flag = True

        enough_minimum = False
        est_ord_sw_off = self.minimal_sewage_ord(self.ord_bottom.value)
        expedient_ord_sw_on = round(
            self.ord_inlet.value - self.difference_in_start.value, 2)

        start_params = self.work_point(
                self.average_flow(self.inflow_max, self.inflow_min),
                expedient_ord_sw_on,
                self.n_of_pumps)

        '''
        while not enough_minimum:
            pumpset_params = self.pumpset_parameters(est_ord_sw_off, 'm')
            ord_sw_on_diff = expedient_ord_sw_on - pumpset_params[str(
                self.n_of_pumps)]['ord_sw_on']

            log.debug('number of pumps: {}'.format(self.n_of_pumps))
            log.debug('est_ord_sw_off: {}'.format(est_ord_sw_off))
            log.debug('ORD_SW_OFF_DIFF: {}'.format(ord_sw_on_diff))
            log.debug('expedient_ord_sw_on: {}'.format(expedient_ord_sw_on))
            log.debug('actual ord sw on: {}'.format(pumpset_params[str(
                self.n_of_pumps)]['ord_sw_on']))
            log.debug('volume active: {}'.format(self.velocity(
                pumpset_params[str(
                    self.n_of_pumps)]['ord_sw_on'] - est_ord_sw_off)))

            if ord_sw_on_diff > 0.01 or ord_sw_on_diff < -0.005:
                est_ord_sw_off += 0.8 * ord_sw_on_diff
            else:
                log.debug('FOUND ORDS')
                self.work_parameters = pumpset_params
                self.ord_sw_off = est_ord_sw_off
                self.ord_bottom.value = self.ord_sw_off - \
                    self.minimal_sewage_level.value
                enough_minimum = True
        '''

        return validation_flag

    def calc_checking(self):

        log.error('CALC_CHECKING')
        validation_flag = True
        self.ord_sw_off = self.minimal_sewage_ord(self.ord_bottom.value)

        self.work_parameters = self.pumpset_parameters(self.ord_sw_off, 'c')

        return validation_flag

    def calc_optimalisation(self):

        pass

    def ord_bottom_minimal(self, expedient_ord_sw_on):
        ''' Returns ordinate that slightly meets the requirementes of pumping
        volume and useful volume

        It uses variables similar to pumpset_parameters function. Also core is
        similar to those. The point of this one function is to find only the
        last one pump, and its switching off ordinate.

        It mainly works as loop, iterating thru useful height, until it finds
        volume which satisfy cycle time requirements. If that stop parameters
        didn't counterbalance maximum inflow, it attunes another pump, and does
        iterate over heights in new conditions. After finding number of
        requireing pumps it gets switching off ordinate, and sets mini

        '''
        ord_bottom = 0
        enough_pumps = False
        n_of_pumps = 1

        while not enough_pumps:
            self.set_min_dims_as_current(n_of_pumps)

            start_params = self.work_parameters(
                self.average_flow(self.inflow_max, self.inflow_min),
                expedient_ord_sw_on,
                self.n_of_pumps)

            enough_time = False

            if self.n_of_pumps == 1:
                iter_height = 0.1
            else:
                iter_height = expedient_ord_sw_on - parameters[str(
                    self.n_of_pumps - 1)]['ord_sw_off'] + 0.01

            while not enough_time:

                ord_to_check = expedient_ord_sw_on - iter_height
                log.error('ord_to_check : {}\n'.format(ord_to_check))

                stop_params = self.work_point(
                    self.average_flow(self.inflow_max, self.inflow_min),
                    ord_to_check,
                    n_of_pumps)

                pump_flow = v.CalcFlow(stop_params[2].v_lps + (
                    (start_params[2].v_lps - stop_params[2].v_lps) / 2),
                    unit="liters")
                inflow = self.get_worst_case_inflow(pump_flow)
                volume_useful = self.velocity(ord_to_check - ord_sw_off)
                cycle_times = self.get_cycle_times(
                    volume_active, pump_flow, inflow)

                if cycle_times[0] > self.pump.cycle_time_s:
                    enough_time = True
                    log.error('ENOUGH TIME ')
                else:
                    iter_height += self.adjust_h_step(volume_useful, pump_flow)

            # do stuff

            if stop_params[2].v_lps >= self.inflow_max.v_lps:
                enough_pumps = True
                ord_bottom = ord_to_check
            else:
                n_of_pumps += 1
        return ord_bottom

    def pumpset_parameters(self, ord_sw_off):
        ''' Returns dict of parameters. Keys of the dict are str of pump numbers.
        Values are also dicts, which keys are parameters strings:
        - 'stop' - work_parameters values for proper pumps num for stop
                   ordinate
        - 'start' - work_parameters values for proper pumps num for start
                    ordinate
        - 'ord_sw_on' - ordinate of proper pump num start
        - 'vol_a' - useful volume for proper pump num (pump, not set of pumps)
        - 'times' - tuple returned from get_cycle_times, Cycle Time, Layover
                    Time, Working Time
        - 'worst_infl' - value of get_worst_case_inflow (type == CalcFlow)

        args:
        * ord_sw_off - ordinate, where pump has to stop

        It mainly works as loop, iterating thru useful height, until it finds
        volume which satisfy cycle time requirements. If that stop parameters
        didn't counterbalance maximum inflow, it attunes another pump, and does
        iterate over heights in new conditions. After finding number of
        requireing pumps it saves founded parameters of all pumps.

        '''

        self.n_of_pumps = 1
        enough_pumps = False
        parameters = {}

        while not enough_pumps:
            parameters[str(self.n_of_pumps)] = {}

            stop_params = self.work_point(
                self.average_flow(self.inflow_max, self.inflow_min),
                ord_sw_off,
                self.n_of_pumps)

            parameters[str(self.n_of_pumps)]['stop'] = stop_params

            enough_time = False

            if self.n_of_pumps == 1:
                iter_height = 0.1
            else:
                last_pump_on = parameters[str(
                    self.n_of_pumps - 1)]['ord_sw_on']
                iter_height = last_pump_on - ord_sw_off

            while not enough_time:
                ord_to_check = ord_sw_off + iter_height
                log.error('ord_to_check : {}'.format(ord_to_check))

                start_params = self.work_point(
                    self.average_flow(self.inflow_max, self.inflow_min),
                    ord_to_check, self.n_of_pumps)

                pump_flow = v.CalcFlow(stop_params[2].v_lps + (
                    (start_params[2].v_lps - stop_params[2].v_lps) / 2),
                    unit="liters")
                inflow = self.get_worst_case_inflow(pump_flow)
                if self.n_of_pumps == 1:
                    lower_va_ord = ord_sw_off
                else:
                    lower_va_ord = parameters[str(
                        self.n_of_pumps - 1)]['ord_sw_on']
                log.debug('lower_va_ord: {}'.format(lower_va_ord))
                this_pump_vol_useful = self.velocity(
                    ord_to_check - lower_va_ord)
                pumpset_vol_useful = self.velocity(ord_to_check - ord_sw_off)
                log.debug('volume_active: {}'.format(this_pump_vol_useful))
                cycle_times = self.get_cycle_times(
                    pumpset_vol_useful, pump_flow, inflow)

                if cycle_times[0] > self.pump.cycle_time_s:
                    enough_time = True
                    log.error('ENOUGH TIME ')
                else:
                    iter_height += self.adjust_h_step(volume_active, pump_flow)

            parameters[str(self.n_of_pumps)]['start'] = start_params
            parameters[str(self.n_of_pumps)]['times'] = cycle_times
            parameters[str(self.n_of_pumps)]['vol_a'] = volume_active
            parameters[str(self.n_of_pumps)]['ord_sw_on'] = ord_to_check
            parameters[str(self.n_of_pumps)]['worst_infl'] = inflow

            if stop_params[2].v_lps >= self.inflow_max.v_lps:
                enough_pumps = True
            else:
                self.n_of_pumps += 1

        return parameters

    def minimalisation_parameters(self):
        enough_pumps = False
        self.n_of_pumps = 1
        parameters = {}
        self.set_min_dims_as_current(self.n_of_pumps)
        ord_minimal = self.ord_inlet.value - 

        while not enough_pumps:

            start_params = self.work_point(
                self.average_flow(self.inflow_max, self.inflow_min),
                ord_minimal, self.n_of_pumps)

        return parameters

    def work_point(self, start_Qp, sewage_ord, pump_no):
        """ Returns tuple of work parameters:
        (LC highness, geometric highness, flow, speed in collector,
        speed in discharge)

        Kolejne iteracje modyfikują parametr przepływu, dopóki nie zostanie
        znaleziony taki, w którego funkcji odpowiednio blisko będą:
        -wys. podnoszenia pompy
        -poziom dynamicznych strat ciśnienia w przewodzie
        """
        geometric_height = self.ord_upper_level.value - sewage_ord

        log.debug('\n\n\nWORK PARAMETERES CALCULATING\n\n\n')
        log.debug('geometric_height: {} - {} = {}'.format(
            self.ord_upper_level.value, sewage_ord, geometric_height))

        iter_Qp = start_Qp
        step = 0.05
        close_enough = False

        pump_x = calc.get_x_axis(self, 'liters')
        p_flows, p_lifts = self.pump.characteristic.get_pump_char_func(pump_no)
        p_flows_vals = [flow.v_lps for flow in p_flows]
        pump_y = calc.fit_coords(p_flows_vals, p_lifts, 3)(pump_x)
        log.debug("pump x: {} len {}, pump y: {} len {}".format(
            pump_x, len(pump_x), pump_y, len(pump_y)))

        while not close_enough:
            log.debug('\n\n\nLOOP WHILE - Calculating parameters\n\n\n')
            log.debug('Flow : {}'.format(iter_Qp))

            log.debug('geometric_height: {}'.format(geometric_height))
            log.debug('ins_pipe sum_loss: {}'.format(self.ins_pipe.sum_loss(
                iter_Qp)))
            log.debug('out_pipe sum_loss: {}'.format(self.out_pipe.sum_loss(
                iter_Qp)))
            pipe_val = geometric_height + self.ins_pipe.sum_loss(
                iter_Qp) + self.out_pipe.sum_loss(iter_Qp)
            pump_val = calc.interp(iter_Qp, pump_x, pump_y)
            log.debug('pipe_val : {}'.format(pipe_val))
            log.debug('pump_val : {}'.format(pump_val))

            difference = pump_val - pipe_val
            log.debug('oldstep: {}'.format(step))
            log.debug('difference: {}'.format(difference))
            step = self.adjust_q_step(difference, step, pump_no)
            log.debug('newstep: {}'.format(step))

            if difference < -0.2:
                log.debug('difference < 0.1: {}'.format(difference))
                iter_Qp.value += step
                log.debug('new iterQp: {}\n\n'.format(iter_Qp))
            elif difference > 0.2:
                log.debug('difference > 0.1: {}'.format(difference))
                iter_Qp.value += step
                log.debug('new iterQp: {}\n\n'.format(iter_Qp))
            else:
                log.error(
                    'FOUND PARAMS for sewage_ord {} for pump {}\n\n'.format(
                        sewage_ord, pump_no))
                close_enough = True

        calc_Qp = iter_Qp
        speed_out_pipe = (calc_Qp.value * 0.001) / self.out_pipe.get_area()
        speed_ins_pipe = (calc_Qp.value * 0.001) / self.ins_pipe.get_area()

        return (pump_val, geometric_height, calc_Qp, speed_out_pipe,
                speed_ins_pipe)

    def adjust_q_step(self, diff, old_step, pump_no):
        '''
        '''
        flow_coords, lift_coords = self.pump.characteristic.get_pump_char_func(
            pump_no)
        log.debug('flow coords: {}, lift_coords: {}'.format(
            flow_coords, lift_coords))
        base_step = ((flow_coords[-1].v_lps - flow_coords[0].v_lps) /
                     (lift_coords[0] - lift_coords[-1])) / 2
        log.debug('base_step: {}'.format(base_step))
        return round(base_step * diff, 2)

    def adjust_h_step(self, iterated_v, qp):
        sought_v = (self.pump.cycle_time.value * 60 * qp.v_m3ps) / 4
        delta_v = sought_v - iterated_v
        h_step = round(0.6 * (delta_v / self.well.area), 2)
        if h_step < 0.01:
            h_step = 0.01
        log.debug('adjusted h step to: {}, based on sought va {}'.format(
            h_step, sought_v))
        return h_step

    def get_cycle_times(self, volume_active, pump_flow, inflow):
        pumping_time = round(volume_active / (
            pump_flow.v_m3ps - inflow.v_m3ps), 1)
        layover_time = round(volume_active / inflow.v_m3ps, 1)
        cycle_time = layover_time + pumping_time

        return cycle_time, layover_time, pumping_time

    def set_min_dims_as_current(self, n_of_pumps):
        self.n_of_res_pumps = self.reserve_pumps_number(
            self.reserve_pumps.value, n_of_pumps)
        self.well.update_min_dimensions(
            self.well.shape.value,
            n_of_pumps + self.n_of_res_pumps,
            self.pump.contour.value,
            self.well.config.value)
        self.well.diameter.value = self.well.min_diameter
        self.well.length.value = self.well.min_length
        self.well.width.value = self.well.min_width
        self.well.update()

    def get_worst_case_inflow(self, pump_flow):

        half_pump_flow = pump_flow.v_lps / 2

        if (half_pump_flow <= self.inflow_max.v_lps and
                half_pump_flow >= self.inflow_min.v_lps):
            result = half_pump_flow
        elif half_pump_flow < self.inflow_min.v_lps:
            result = self.inflow_min.v_lps
        elif half_pump_flow > self.inflow_max.v_lps:
            result = self.inflow_max.v_lps

        worst_inflow = v.CalcFlow(result, "liters")
        return worst_inflow

    def reserve_pumps_number(self, variant, work_pumps_no):
        """Sets number of reserve pumps, based on user choose"""
        if variant == 'minimal':
            n_of_res_pumps = 1
        elif variant == 'optimal':
            if work_pumps_no % 2 == 0:
                n_of_res_pumps = int(work_pumps_no / 2)
            else:
                n_of_res_pumps = int(work_pumps_no / 2) + 1
        elif variant == 'safe':
            n_of_res_pumps = work_pumps_no
        return n_of_res_pumps
