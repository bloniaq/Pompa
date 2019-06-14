# libraries
import logging

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

    def update(self):
        self.well.update()
        self.pump.update()
        self.ins_pipe.update()
        self.out_pipe.update()

        pass

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
        validation_flag = True

        calculations = {'minimalisation': self.calc_minimalisation(),
                        'checking': self.calc_checking(),
                        'optimalisation': self.calc_optimalisation()}

        self.update()

        station.qp = station.get_calculative_flow()

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

        enough = False
        while not enough:
            log.debug('inflow max [lps]: {}'.format(self.inflow_max.v_lps))
            log.debug('inflow min [lps]: {}'.format(self.inflow_min.v_lps))
            log.debug('ord sw off [m]: {}'.format(self.ord_sw_off))
            log.debug('n of pumps: {}'.format(self.n_of_pumps))
            stop_params = self.get_work_parameters(
                self.average_flow(self.inflow_max, self.inflow_min),
                self.ord_sw_off,
                self.n_of_pumps)

            if stop_params[2].v_lps < self.inflow_max.v_lps:
                enough = True
            else:
                self.n_of_pumps += 1

        return validation_flag

    def calc_optimalisation(self):

        pass

    def get_work_parameters(self, flow_var, start_ord, pump_no):
        """ Returns tuple of work parameters:
        (LC highness, geometric highness, flow, speed in collector,
         speed in discharge)
        """
        geom_H = self.ord_upper_level.value - start_ord
        log.debug('geomH: {} - {} = {}'.format(
            self.ord_upper_level.value, start_ord, geom_H))
        flow = v.CalcFlow(flow_var.v_lps, unit="liters")
        difference = 100
        step = 0.05
        pump_x = calc.get_x_axis(self, 'liters')
        flows, lifts = self.pump.characteristic.get_pump_char_func()
        flows_vals = [flow.v_lps for flow in flows]
        pump_y = calc.fit_coords(flows_vals, lifts, 3)(pump_x)
        log.debug("pump x: {} len {}, pump y: {} len {}".format(
            pump_x, len(pump_x), pump_y, len(pump_y)))
        log.debug('WE\'RE IN LOOP')
        while True:
            log.debug('LOOP WHILE')
            log.debug('Flow : {}'.format(flow))
            pipe_val = geom_H + self.ins_pipe.sum_loss(
                flow) + self.out_pipe.sum_loss(flow)
            pump_val = calc.interp(flow, pump_x, pump_y)
            log.debug('pipe_val : {}'.format(pipe_val))
            log.debug('pump_val : {}'.format(pump_val))
            difference = pump_val - pipe_val
            if difference < -0.1:
                log.debug('difference < 0.1: {}'.format(difference))
                flow = flow - step
            elif difference > 0.1:
                log.debug('difference > 0.1: {}'.format(difference))
                flow = flow + step
            else:
                break
        speed_coll = (flow * 0.001) / self.out_pipe.get_area()
        speed_dpipe = (flow * 0.001) / self.ins_pipe.get_area()
        flow_var = v.CalcFlow(flow, unit="liters")
        return pump_val, geom_H, flow_var, speed_coll, speed_dpipe
