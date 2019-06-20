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

    def minimal_sewage_ord(self):
        return self.ord_bottom.value + self.minimal_sewage_level.value

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

    def pump_set_ready(self):
        flag = True
        if self.pump_set is None:
            flag = False
        if self.number_of_pumps == 1:
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

        calculations = {'minimalisation': self.calc_minimalisation(),
                        'checking': self.calc_checking(),
                        'optimalisation': self.calc_optimalisation()}

        validation_flag = calculations[mode]

        self.h_whole = self.ord_terrain.value - self.ord_bottom.value
        self.v_whole = self.velocity(self.h_whole)
        self.h_useful = self.work_parameters[str(
            self.n_of_pumps)]['ord_sw_on'] - self.ord_sw_off
        self.v_useful = self.velocity(self.h_useful)

        self.ord_sw_on = self.work_parameters[str(
            self.n_of_pumps)]['ord_sw_on']
        self.ord_sw_alarm = self.ord_inlet.value
        self.h_reserve = self.ord_sw_alarm - self.ord_sw_on
        if self.h_reserve < 0:
            self.statement += '\nUWAGA! Rzędna włączenia pomp powyżej dna ' + \
                'przewodu doprowadzającego ścieki do pompowni\n\n'
        self.v_reserve = self.velocity(self.h_reserve)

        self.v_dead = self.velocity(self.minimal_sewage_level.value)
        self.n_of_res_pumps = calc.reserve_pumps_number(self)
        self.statement += self.well.update_min_dimensions(
            self.well.shape.value,
            self.n_of_pumps + self.n_of_res_pumps,
            self.pump.contour.value,
            self.well.config.value)

        return validation_flag

    def calc_minimalisation(self):

        pass

    def calc_checking(self):
        validation_flag = True

        self.ord_sw_off = self.minimal_sewage_ord()
        self.n_of_pumps = 1

        enough_pumps = False

        COUNTER = 0
        # tylko dla testów, do usunięcie

        __parameters = {}

        while not enough_pumps:
            __parameters[str(self.n_of_pumps)] = {}

            log.debug('inflow max [lps]: {}'.format(self.inflow_max.v_lps))
            log.debug('inflow min [lps]: {}'.format(self.inflow_min.v_lps))
            log.debug('ord sw off [m]: {}'.format(self.ord_sw_off))
            log.debug('n of pumps: {}'.format(self.n_of_pumps))
            stop_params = self.get_work_parameters(
                self.average_flow(self.inflow_max, self.inflow_min),
                self.ord_sw_off,
                self.n_of_pumps)

            __parameters[str(self.n_of_pumps)]['stop'] = stop_params

            enough_time = False
            if self.n_of_pumps == 1:
                iter_height = 0.1
            else:
                last_pump_on = __parameters[str(
                    self.n_of_pumps - 1)]['ord_sw_on']
                iter_height = last_pump_on - self.ord_sw_off
                log.error('iter_height : {}'.format(iter_height))

            while not enough_time:
                ord_to_check = self.ord_sw_off + iter_height
                log.error('ord_to_check : {}'.format(ord_to_check))

                start_params = self.get_work_parameters(
                    self.average_flow(self.inflow_max, self.inflow_min),
                    ord_to_check, self.n_of_pumps)

                pump_flow = v.CalcFlow(stop_params[2].v_lps + (
                    (start_params[2].v_lps - stop_params[2].v_lps) / 2),
                    unit="liters")
                inflow = self.get_worst_case_inflow(pump_flow)
                if self.n_of_pumps == 1:
                    lower_va_ord = self.ord_sw_off
                else:
                    lower_va_ord = __parameters[str(
                        self.n_of_pumps - 1)]['ord_sw_on']
                log.debug('lower_va_ord: {}'.format(lower_va_ord))
                volume_active = self.velocity(ord_to_check - lower_va_ord)
                log.debug('volume_active: {}'.format(volume_active))
                cycle_times = self.get_cycle_times(
                    volume_active, pump_flow, inflow)

                if cycle_times[0] > self.pump.cycle_time_s:
                    enough_time = True
                    log.error('ENOUGH TIME ')
                else:
                    iter_height += self.adjust_h_step(volume_active, pump_flow)

            __parameters[str(self.n_of_pumps)]['start'] = start_params
            __parameters[str(self.n_of_pumps)]['times'] = cycle_times
            __parameters[str(self.n_of_pumps)]['vol_a'] = volume_active
            __parameters[str(self.n_of_pumps)]['ord_sw_on'] = ord_to_check
            __parameters[str(self.n_of_pumps)]['worst_infl'] = inflow

            COUNTER += 1

            if stop_params[2].v_lps > self.inflow_max.v_lps:
                enough_pumps = True

            elif COUNTER == 9:
                enough_pumps = True
            else:
                self.n_of_pumps += 1

        self.work_parameters = __parameters
        return validation_flag

    def calc_optimalisation(self):

        pass

    def get_work_parameters(self, start_Qp, sewage_ord, pump_no):
        """ Returns tuple of work parameters:
        (LC highness, geometric highness, flow, speed in collector,
        speed in discharge)

        Kolejne iteracje modyfikują parametr przepływu, dopóki nie zostanie
        znaleziony taki, w którego funkcji odpowiednio blisko będą:
        -wys. podnoszenia pompy
        -poziom dynamicznych strat ciśnienia w przewodzie
        """
        geometric_height = self.ord_upper_level.value - sewage_ord

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
            log.debug('LOOP WHILE - Calculating parameters')
            log.debug('Flow : {}'.format(iter_Qp))

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
                iter_Qp.value -= step
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
        OLD VERSION
        log.info("0.1 * math.fabs(diff): {}".format(0.1 * math.fabs(diff)))
        if 0.1 * math.fabs(diff) <= old_step:
            new_step = 0.03
        else:
            new_step = 0.5 * math.fabs(diff)
        return new_step

        średnia wartość deltaQ dla deltaH = 1
        '''
        flow_coords, lift_coords = self.pump.characteristic.get_pump_char_func(
            pump_no)
        log.debug('flow coords: {}, lift_coords: {}'.format(
            flow_coords, lift_coords))
        base_step = ((flow_coords[-1].v_lps - flow_coords[0].v_lps) /
                     (lift_coords[0] - lift_coords[-1])) / 2
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
