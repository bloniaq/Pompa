# libraries
import logging
import numpy as np

# modules
import components
import maths
import output as o

log = logging.getLogger('Pompa.station')


class Station(components.StationObject):

    def __init__(self, app):
        super().__init__(app)

        # components
        self.well = None
        self.d_pipe = None
        self.coll = None
        self.pump_type = None
        self.pump_set = None
        self.pumps = []

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

        # parameters to calculate
        self.number_of_pumps = None
        self.number_of_res_pumps = None
        self.height_start = None
        self.height_stop = None
        self.ord_sw_on = None
        self.ord_sw_off = None
        self.ord_sw_alarm = None
        self.comp_flow = None

    '''
    def calc_checking(self):
        # get working pump numbers
        self.number_of_pumps = self.calc_number_of_pumps()
        # get reserve pump numbers
        self.number_of_res_pumps = self.reserve_pumps_number()
        # get ordinate off
        self.ord_sw_off = self.ord_bottom.value +\
            self.minimal_sewage_level.value
        # Setting up Pump Set
        self.pump_set = components.PumpSet(self)
        # for pump
        log.debug('CALC CHECKING FINISHED')
        pass

    
    def calculate(self):
=======
    def calculate_checking(self):
>>>>>>> 91e599add284f764b6373d33b35d15b0f77070cf
        """calculates parameters of working pump station"""
        self.v_useful = self.check_get_useful_velo()
        self.h_useful = self.v_useful / self.well.cross_sectional_area()
        self.number_of_pumps = self.calc_number_of_pumps()
        self.number_of_res_pumps = self.reserve_pumps_number()
        self.ord_sw_on = self.ord_inlet.value - 0.1
        self.ord_sw_off = self.ord_bottom.value +\
            self.minimal_sewage_level.value
        self.ord_sw_alarm = self.ord_inlet.value
        self.height_start = self.height_to_pump(self.ord_sw_off)
        self.height_stop = self.height_to_pump(self.ord_sw_on)
        self.qp = self.get_calculative_flow()
        self.h_whole = self.ord_terrain.value - self.ord_bottom.value
        self.h_reserve = self.ord_sw_alarm - self.ord_sw_on
        self.v_whole = self.velocity(self.h_whole)
        self.v_dead = self.velocity(self.minimal_sewage_level.value)
        self.v_reserve = self.velocity(self.h_reserve)
        self.comp_flow = self.get_calculative_flow()
    '''

    def height_to_pump(self, lower_ord):
        height = self.ord_upper_level.value - lower_ord
        return height

    def calc_number_of_pumps(self):
        """Sets number of work pumps, based on min and max inflow, and pump
        efficiency

        TO MAKE TEST THIS FUNCTION!
        """
        log.debug('calc_number_of_pumps START')
        max_pump_eff = self.pump_type.max_pump_efficiency()
        log.debug('minimal inflow value_liters {}'.format(
            self.inflow_min.value_liters))
        if max_pump_eff.value_liters < self.inflow_min.value_liters:
            log.error('Too low pump efficiency !!!')
            ##############################
            # EXCEPTION TO RAISE !!!
            ##############################
            log.error('Pump has too less efficiency to this station')
            return 0
        number_of_pumps = int(np.ceil((1.1 * self.inflow_max.value_liters) /
                                      max_pump_eff.value_liters))
        log.debug('Result: {}'.format(number_of_pumps))
        self.number_of_pumps = number_of_pumps
        return number_of_pumps

    def reserve_pumps_number(self):
        """Sets number of reserve pumps, based on user choose"""
        if self.reserve_pumps.value == 'minimal':
            n_of_res_pumps = 1
        elif self.reserve_pumps.value == 'optimal':
            if self.number_of_pumps % 2 == 0:
                n_of_res_pumps = int(self.number_of_pumps / 2)
            else:
                n_of_res_pumps = int(self.number_of_pumps / 2) + 1
        elif self.reserve_pumps.value == 'safe':
            n_of_res_pumps = self.number_of_pumps
        self.number_of_res_pumps = n_of_res_pumps
        return n_of_res_pumps

    def check_get_useful_velo(self):
        useful_velo = ((((
            self.pump_type.cycle_time.value) * 60) * self.qp) / 4000)
        log.info('useful velo is {}m3'.format(useful_velo))
        return useful_velo

    def get_x_axis(self, unit, n=1):
        if unit == 'meters':
            inflow_val_min = self.inflow_min.value_meters
            inflow_val_max = self.inflow_max.value_meters
            eff_from = self.pump_type.efficiency_from.value_meters
            eff_to = self.pump_type.efficiency_to.value_meters
        elif unit == 'liters':
            inflow_val_min = self.inflow_min.value_liters
            inflow_val_max = self.inflow_max.value_liters
            eff_from = self.pump_type.efficiency_from.value_liters
            eff_to = self.pump_type.efficiency_to.value_liters
        x_min = min(inflow_val_min - 3, eff_from - 3)
        if x_min < 0:
            x_min = 0
        x_max = max(1.5 * (inflow_val_max + 3), 1.5 * (eff_to + 3),
                    n * (inflow_val_max + 3))
        return np.linspace(x_min, x_max, 200)

    def pipes_ready(self):
        log.debug('Are pipes ready?')
        flag = True
        if not self.d_pipe.pipe_char_ready():
            flag = False
        log.debug(flag)
        if not self.collector.pipe_char_ready():
            flag = False
        log.debug(flag)
        return flag

    def get_all_pipes_char_vals(self, unit):
        log.debug('Starting draw_pipes_plot')
        flows, _ = self.pump_type.characteristic.get_pump_char_func(unit)
        log.debug('Got geometric loss')
        discharge_y = self.d_pipe.get_y_coords(flows, unit)
        log.debug('Got discharge_pipe ys')
        collector_y = self.collector.get_y_coords(flows, unit)
        log.debug('Got collector ys')
        pipes_char = []
        for i in range(len(flows)):
            sum_l = discharge_y[i] + collector_y[i]
            pipes_char.append(sum_l)
        y = maths.fit_coords(flows, pipes_char, 2)
        return y

    def get_geom_loss_vector(self):
        log.debug('Starting draw_pipes_plot')
        flows, _ = self.pump_type.characteristic.get_pump_char_func('liters')
        loss_char = []
        geom_loss = self.height_to_pump(
            self.ord_bottom.value + self.minimal_sewage_level.value)
        for i in range(len(flows)):
            loss_char.append(geom_loss)
        y = maths.fit_coords(flows, loss_char, 1)
        return y

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

    def get_work_parameters(self, flow, start_ord):
        """ Returns tuple of work parameters:
        (LC highness, geometric highness, flow, speed in collector,
         speed in discharge)
        """
        start_ordi = self.ord_bottom.value + self.minimal_sewage_level.value
        geom_H = self.ord_upper_level.value - start_ordi
        # flow = flow.value_liters  # l/s
        difference = 100
        step = 0.05
        pump_x = self.get_x_axis('liters')
        flows, lifts = self.pump_type.characteristic.get_pump_char_func(
            "liters")
        pump_y = maths.fit_coords(flows, lifts, 3)(pump_x)
        log.debug("pump x: {} len {}, pump y: {} len {}".format(
            pump_x, len(pump_x), pump_y, len(pump_y)))
        log.debug('WE\'RE IN LOOP')
        while True:
            log.debug('LOOP WHILE')
            log.debug('Flow : {}'.format(flow))
            pipe_val = geom_H + self.d_pipe.sum_loss(
                flow, "liters") + self.collector.sum_loss(flow, "liters")
            pump_val = maths.interp(flow, pump_x, pump_y)
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
        speed_coll = (flow * 0.001) / self.collector.get_area()
        speed_dpipe = (flow * 0.001) / self.d_pipe.get_area()
        return pump_val, geom_H, flow, speed_coll, speed_dpipe

    def data_check(self, mode):
        """ Returns boolean of validation

        Checking if all data needed to calculate in chosen mode is filled,
        and correct.
        """

        validation_flag = True
        # TODO:
        # Validation procesess
        return validation_flag

    def calculate(self, mode):
        """ Returns validation flag

        Runs calculations and checks if results exists and if are correct.
        """

        calculations = {'minimalisation': self.calc_minimalisation(),
                        'checking': self.calc_checking(),
                        'optimalisation': self.calc_optimalisation()}

        validation_flag = True
        n = self.calc_number_of_pumps()
        if n <= 0:
            validation_flag = False
        n = self.reserve_pumps_number()
        if n <= 0:
            validation_flag = False
        self.qp = self.get_calculative_flow()
        self.v_useful = self.check_get_useful_velo()
        self.h_useful = self.v_useful / self.well.cross_sectional_area()
        self.number_of_pumps = self.calc_number_of_pumps()
        self.number_of_res_pumps = self.reserve_pumps_number()
        self.ord_sw_on = self.ord_inlet.value - 0.1
        self.ord_sw_off = self.ord_bottom.value +\
            self.minimal_sewage_level.value
        self.ord_sw_alarm = self.ord_inlet.value
        self.height_start = self.height_to_pump(self.ord_sw_off)
        self.height_stop = self.height_to_pump(self.ord_sw_on)
        self.h_whole = self.ord_terrain.value - self.ord_bottom.value
        self.h_reserve = self.ord_sw_alarm - self.ord_sw_on
        self.v_whole = self.velocity(self.h_whole)
        self.v_dead = self.velocity(self.minimal_sewage_level.value)
        self.v_reserve = self.velocity(self.h_reserve)
        self.comp_flow = self.get_calculative_flow()
        # TODO:
        # Calculations
        return validation_flag

    def generate_report(self, mode):
        """ Returns report content in string
        """
        report = ""
        # TODO:
        # Report making processes
        if mode == 'checking':
            report = o.generate_checking_report(self)
        return report
