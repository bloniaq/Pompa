# libraries
import logging
import math

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
        self.work_parameters

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
        velocity = self.well.cross_sectional_area() * height
        log.debug('v for h: {} is {}'.format(height, velocity))
        return velocity

    def get_calculative_flow(self):
        return self.inflow_max.value_liters * 1.4

    def calculate(self, mode):
        """ Returns validation flag

        Runs calculations and checks if results exists and if are correct.
        """
        self.update()
        validation_flag = True

        calculations = {'minimalisation': self.calc_minimalisation(),
                        'checking': self.calc_checking(),
                        'optimalisation': self.calc_optimalisation()}


        # station.qp = station.get_calculative_flow()

        validation_flag = calculations[mode]
        # station.v_useful = check_get_useful_velo()
        # station.h_useful = station.v_useful / station.well.cross_sectional_area()
        # station.number_of_pumps = calc_number_of_pumps()
        # station.number_of_res_pumps = reserve_pumps_number()
        # station.ord_sw_on = station.ord_inlet.value - 0.1
        # station.ord_sw_off = station.ord_bottom.value +\
        #     station.minimal_sewage_level.value
        # station.ord_sw_alarm = station.ord_inlet.value
        # station.height_start = station.height_to_pump(station.ord_sw_off)
        # station.height_stop = station.height_to_pump(station.ord_sw_on)
        # station.h_whole = station.ord_terrain.value - station.ord_bottom.value
        # station.h_reserve = station.ord_sw_alarm - station.ord_sw_on
        # station.v_whole = station.velocity(station.h_whole)
        # station.v_dead = station.velocity(station.minimal_sewage_level.value)
        # station.v_reserve = station.velocity(station.h_reserve)
        # TODO:
        # Calculations

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
            iter_height = 0.1

            while not enough_time:
                ord_to_check = self.ord_sw_off + iter_height

                start_params = self.get_work_parameters(
                    self.average_flow(self.inflow_max, self.inflow_min),
                    ord_to_check, self.n_of_pumps)

                pump_flow = start_params[2]
                inflow = self.get_worst_case_inflow(pump_flow)
                cycle_times = self.get_cycle_times(
                    ord_to_check, self.ord_sw_off, pump_flow, inflow)

                if cycle_times[0] > self.pump.cycle_time_s:
                    enough_time = True
                else:
                    iter_height += 0.01

            __parameters[str(self.n_of_pumps)]['start'] = start_params
            __parameters[str(self.n_of_pumps)]['times'] = cycle_times
            __parameters[str(self.n_of_pumps)]['ord_sw_on'] = ord_to_check

            COUNTER += 1

            if stop_params[2].v_lps < self.inflow_max.v_lps:
                enough_pumps = True

            elif COUNTER == 6:
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
        """
        geometric_height = self.ord_upper_level.value - sewage_ord
        log.debug('geometric_height: {} - {} = {}'.format(
            self.ord_upper_level.value, sewage_ord, geometric_height))

        iter_Qp = start_Qp
        step = 0.05

        pump_x = calc.get_x_axis(self, 'liters')
        p_flows, p_lifts = self.pump.characteristic.get_pump_char_func()
        p_flows_vals = [flow.v_lps for flow in p_flows]
        pump_y = calc.fit_coords(p_flows_vals, p_lifts, 3)(pump_x)
        log.debug("pump x: {} len {}, pump y: {} len {}".format(
            pump_x, len(pump_x), pump_y, len(pump_y)))

        log.debug('WE\'RE IN LOOP')
        while True:
            log.debug('LOOP WHILE')
            log.debug('Flow : {}'.format(iter_Qp))

            pipe_val = geometric_height + self.ins_pipe.sum_loss(
                iter_Qp) + self.out_pipe.sum_loss(iter_Qp)
            pump_val = calc.interp(iter_Qp, pump_x, pump_y)
            log.debug('pipe_val : {}'.format(pipe_val))
            log.debug('pump_val : {}'.format(pump_val))

            difference = pump_val - pipe_val
            step = self.adjust_step(difference, step)

            if difference < -0.1:
                log.debug('difference < 0.1: {}'.format(difference))
                iter_Qp.value -= step
                log.debug('new iterQp: {}'.format(iter_Qp))
            elif difference > 0.1:
                log.debug('difference > 0.1: {}'.format(difference))
                iter_Qp.value += step
                log.debug('new iterQp: {}'.format(iter_Qp))
            else:
                break
        calc_Qp = iter_Qp
        speed_coll = (calc_Qp.value * 0.001) / self.out_pipe.get_area()
        speed_dpipe = (calc_Qp.value * 0.001) / self.ins_pipe.get_area()
        # flow_var = v.CalcFlow(flow, unit="liters")
        return pump_val, geometric_height, calc_Qp, speed_coll, speed_dpipe

    def adjust_step(self, diff, old_step):
        if 0.1 * diff <= old_step:
            new_step = 0.05
        else:
            new_step = 0.5 * diff
        return new_step

    def get_cycle_times(self, ord1, ord2, pump_flow, inflow):
        volume_active = round(math.fabs(ord1 - ord2) * self.well.area, 3)
        pumping_time = round(volume_active / (
            pump_flow.v_m3ps - inflow.v_m3ps), 1)
        layover_time = round(volume_active / inflow.v_m3ps, 1)
        cycle_time = layover_time + pumping_time

        return cycle_time, pumping_time, layover_time

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
