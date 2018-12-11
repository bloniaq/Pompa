# libraries
import logging
import numpy as np

# modules
import components
import maths

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
        self.comp_flow = None

    def calculate(self):
        """calculates parameters of working pump station"""
        self.ord_sw_on = self.ord_inlet.value - 0.1  # FILL UP
        self.ord_sw_off = self.ord_bottom.value +\
            self.minimal_sewage_level.value
        self.number_of_pumps = self.calc_number_of_pumps()
        self.number_of_res_pumps = self.reserve_pumps_number()
        self.height_start = self.height_to_pump(self.ord_sw_off)
        self.height_stop = self.height_to_pump(self.ord_sw_on)
        self.qp = self.get_calculative_flow()
        self.h_useful = self.ord_sw_off - self.ord_sw_on  # FILL UP
        self.h_whole = self.ord_terrain.value - self.ord_bottom.value
        self.h_reserve = 0  # FILL UP
        self.v_whole = self.velocity(self.h_whole)
        self.v_useful = self.velocity(self.h_useful)
        self.v_dead = self.velocity(self.minimal_sewage_level.value)
        self.v_reserve = self.velocity(self.h_reserve)
        self.comp_flow = self.get_calculative_flow()

    def height_to_pump(self, lower_ord):
        height = self.ord_upper_level.value - lower_ord
        return height

    def calc_number_of_pumps(self):
        """Sets number of work pumps, based on min and max inflow, and pump
        efficiency"""
        log.debug('Calculating number of pumps')
        max_pump_eff = self.pump_type.max_pump_efficiency()
        log.debug('minimal inflow value_liters {}'.format(
            self.inflow_min.value_liters))
        if max_pump_eff.value_liters < self.inflow_min.value_liters:
            log.error('BŁĄD')
            return 0
        number_of_pumps = int(np.ceil((1.25 * self.inflow_max.value_liters) /
                                      max_pump_eff.value_liters))
        log.debug('Result: {}'.format(number_of_pumps))
        self.number_of_pumps = number_of_pumps
        self.pump_set = components.PumpSet(self)
        return number_of_pumps

    def reserve_pumps_number(self):
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

    def get_x_axis(self, unit):
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
        x_max = max(inflow_val_max + 3, eff_to + 3)
        return np.linspace(x_min, 1.5 * x_max, 200)

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

    def draw_pipes_plot(self, x_lin, unit):
        log.debug('Starting draw_pipes_plot')
        flows, _ = self.pump_type.characteristic.get_pump_char_func()
        geom_loss = self.height_to_pump(
            self.ord_bottom.value + self.minimal_sewage_level.value)
        log.debug('Got geometric loss')
        discharge_y = self.d_pipe.get_y_coords(flows, unit)
        log.debug('Got discharge_pipe ys')
        collector_y = self.collector.get_y_coords(flows, unit)
        log.debug('Got collector ys')
        pipes_char = []
        for i in range(len(flows)):
            pipes_char.append(geom_loss + discharge_y[i] + collector_y[i])
        y = maths.fit_coords(flows, pipes_char, 1)
        return x_lin, y(x_lin), 'g-'

    def velocity(self, height):
        velocity = self.well.cross_sectional_area() * height
        log.debug('v for h: {} is {}'.format(height, velocity))
        return velocity

    def get_calculative_flow(self):
        return self.inflow_max.value * 1.5
