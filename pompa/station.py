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

    def data_check(self, mode):

        flag = True
        # napisać listy zmiennych do sprawdzenia czy są

        checking_list = []
        minimal_list = []
        optimal_list = []

        data_lists = {'checking': checking_list,
                      'minimalisation': minimal_list,
                      'optimalisation': optimal_list}

        for i in data_lists[mode]:
            # napsiać sprawdzanie danych
            pass
        return flag

    def pumps_number(self):
        pass

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

        return number_of_pumps, n_of_res_pumps

    def work_velo(self, flow):
        # time = self.pump.work_time czy coś, byle w s
        time = self.pump_type.cycle_time / 60
        velo = (time * flow) / 4  # flow musi być w m3/s
        area = self.well.cross_sectional_area()  # przekrój ma być w m2
        height = velo / area
        return height

    def get_calculative_flow(self):
        return self.inflow_max.value_liters * 1.4

    def calculation(self, mode):
        if not self.data_check(mode):
            log.info('data check failed')
            return 0
        pumps_n, res_pumps_n = self.calc_number_of_pumps()
        # 2. sprawdz czy sie zmieszcza na tej powierzchni

        # 3. wyznaczenie przepływu startowego
        flow = self.get_calculative_flow()
        end_ord = self.ord_bottom + self.minimal_sewage_level
        if mode == 'checking':
            # 2. oblicz parametry końcowe
            self.end_params = self.get_work_parameters(flow, end_ord)
            # 3. oblicz objetosc dla 1 pompy
            height = self.work_velo(flow)
            # 4. oblicz parametry poczatkowe dla 1 pompy
            self.start_params = self.get_work_parameters(
                flow, end_ord + height)
        elif mode == 'minimalisation':
            pass
        elif mode == 'optimalisation':
            pass
