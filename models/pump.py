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
        flows, lifts = self.characteristic.get_pump_char_func(unit)
        y = self.app.fit_coords(flows, lifts, 3)
        return y

    def generate_pump_char_string(self):
        # patter: 'Q=  {} [l/s]    H=  {} [m]\n'.format()
        char_raport = ''
        for point in self.characteristic.coords:
            q = self.characteristic.coords[point][0].value_liters
            h = self.characteristic.coords[point][1]
            char_raport += 'Q=  {} [l/s]    H=  {} [m]\n'.format(q, h)
        char_raport += '\n'
        return char_raport

    def get_Q_for_H(self, number):
        flows, lifts = self.characteristic.get_pump_char_func('liters')
        set_flows = []
        for flow in flows:
            set_flows.append(flow * number)
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
