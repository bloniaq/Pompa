# libraries
import logging
import numpy as np

# modules
import models.models as models
import models.variables as variables

log = logging.getLogger('pompa.pump')
unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


class PumpType(models.StationObject):
    """class for pumps"""

    def __init__(self, app):
        super().__init__(app)
        self.cycle_time = None
        self.contour = None
        self.suction_level = None
        self.efficiency_from = None
        self.efficiency_to = None
        self.characteristic = None
        self.cycle_time_s = None

    def update(self):
        self.best_eff = self.max_pump_efficiency()
        self.cycle_time_s = self.cycle_time.value * 60

    def set_flow_unit(self, unit):
        log.info('set_flow_unit started')
        unit_bracket = unit_bracket_dict[unit]
        efficiency_from_label = self.ui_vars.__getitem__(
            'pump_efficiency_from_txt')
        efficiency_to_label = self.ui_vars.__getitem__(
            'pump_efficiency_to_txt')
        add_point_label = self.ui_vars.__getitem__(
            'add_point_flow_text')
        efficiency_from_label.set('Od {}'.format(unit_bracket))
        efficiency_to_label.set('Do {}'.format(unit_bracket))
        add_point_label.set('Przepływ Q {}'.format(unit_bracket))
        log.info('self.efficiency_from type: {}'.format(
            type(self.efficiency_from)))
        self.characteristic.set_unit(unit)

    def max_pump_efficiency(self):
        max_eff_val = self.efficiency_from.value_liters + \
            ((self.efficiency_to.value_liters -
                self.efficiency_from.value_liters) / 2)
        max_eff = variables.VFlow(max_eff_val, 'liters')
        log.debug('max eff liters: {}, meters: {}'.format(
            max_eff.value_liters, max_eff.value_meters))
        return max_eff

    def pump_char_ready(self):
        flag = False
        if len(self.characteristic.coords) > 2:
            flag = True
        return flag

    def draw_pump_plot(self):
        unit = self.characteristic.unit_var.get()
        flows, lifts = self.characteristic.get_pump_char_func(1)
        flows_vals = [flow.ret_unit(unit) for flow in flows]
        y = self.app.fit_coords(flows_vals, lifts, 3)
        return y

    def generate_pump_char_string(self):
        # patter: 'Q=  {} [l/s]    H=  {} [m]\n'.format()
        char_raport = ''
        for point in self.characteristic.coords:
            q = self.characteristic.coords[point][0].v_lps
            h = self.characteristic.coords[point][1]
            char_raport += 'Q=  {} [l/s]    H=  {} [m]\n'.format(q, h)
        char_raport += '\n'
        return char_raport

    def get_Q_for_H(self, pump_no):
        flows, lifts = self.characteristic.get_pump_char_func(pump_no)
        set_flows = [flow.v_lps * pump_no for flow in flows]
        log.debug('lifts: {}, flows(in set): {}'.format(lifts, set_flows))
        Qs = self.app.fit_coords(lifts, set_flows, 3)
        log.debug('coords fitted (Qs) : {}'.format(Qs))
        lifts.sort()
        Hs = np.linspace(lifts[0], lifts[-1], 200)
        # log.debug('linspace of H (Hs) : {}'.format(Hs))
        return Hs, Qs

    def get_Q(self, H, Hs, Qs):
        '''
        flows, lifts = self.characteristic.get_pump_char_func('liters')
        set_flows = []
        for flow in flows:
            set_flows.append(flow * number)
        log.debug('lifts: {}, flows(in set): {}'.format(lifts, set_flows))
        Qs = maths.fit_coords(lifts, set_flows, 3)
        log.debug('coords fitted (Qs) : {}'.format(Qs))
        lifts.sort()
        Hs = np.linspace(lifts[0], lifts[-1], 200)
        # log.debug('linspace of H (Hs) : {}'.format(Hs))
        '''
        Q = self.app.interp(H, Hs, Qs(Hs))
        # log.debug('linspace of Q (Qs) : {}'.format(Qs(Hs)))
        log.debug('Q for {}m is {}'.format(H, Q))
        return Q

    def is_flow_in_characteristic(self, flow):
        flows, _ = self.characteristic.get_pump_char_func(1)
        flow_vals = []
        for f in flows:
            flow_vals.append(f.v_lps)
        flow_vals.sort()
        if flow.v_lps < flow_vals[0] or flow.v_lps > flow_vals[-1]:
            return False
        else:
            return True


class PumpSet(models.StationObject):

    def __init__(self, station):
        self.station = station
        # self.well = station.well
        self.n_of_pumps = self.station.number_of_pumps
        self.characteristic = station.pump_type.characteristic
        self.cycle_time = station.pump_type.cycle_time

        self.qp = station.qp
        self.set_start_ordinates()
        self.pumps = []
        self.start_ords = []
        pump_counter = 0
        while pump_counter < self.n_of_pumps:
            log.debug('starting building pump number {}'.format(
                pump_counter + 1))
            pump = Pump(self.station, self, pump_counter + 1)
            self.start_ords.append(pump.get_start_ordinate())
            log.debug('PUMP {} of {} ADDED'.format(
                pump_counter + 1, self.n_of_pumps))
            self.pumps.append(pump)
            log.debug('starts ords: {}'.format(self.start_ords))
            pump_counter += 1
        log.debug('PUMPS IN SET: {}'.format(self.pumps))

    def set_start_ordinates(self):
        self.start_ord_list = []
        self.ord_stop = self.station.ord_bottom.value + \
            self.station.minimal_sewage_level.value
        ord_start = self.station.ord_sw_on  # UZUPEŁNIC
        height = ord_start - self.ord_stop
        self.one_pump_h = round(height / self.n_of_pumps, 2)
        for i in range(self.n_of_pumps):
            ordinate = ord_start + i * self.one_pump_h
            self.start_ord_list.append(ordinate)

    def get_pumpset_vals(self):
        log.debug('Starting draw_pipes_plot')
        flows, lifts = self.characteristic.get_pump_char_func(1)
        n = self.n_of_pumps
        set_flows = [flow.v_lps * n for flow in flows]
        y = self.app.fit_coords(set_flows, lifts, 3)
        return y

