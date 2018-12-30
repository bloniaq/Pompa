# libraries
import logging
import numpy as np

# modules
import maths
import variables

log = logging.getLogger('Pompa.components')
unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


class StationObject():

    kinematic_viscosity = 1.0068  # [mm²/s] dla 20°C
    std_grav = 9.81

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.ui_vars = app.builder.tkvariables

    def __setattr__(self, attr, value):
        if '.' not in attr:
            self.__dict__[attr] = value
        else:
            attr_name, rest = attr.split('.', 1)
            setattr(getattr(self, attr_name), rest, value)

    def __getattr__(self, attr):
        if '.' not in attr:
            log.debug('Has no <.> in attr')
            return super().__getattr__(attr)
        else:
            attr_name, rest = attr.split('.', 1)
            return getattr(getattr(self, attr_name), rest)

    def load_data(self, data_dict):
        for attribute in self.__dict__:
            log.debug('loading {} for obj {}'.format(attribute, self))
            if hasattr(self.__dict__[attribute], 'dan_id'):
                log.debug('{} has dan_id'.format(attribute))
                self.__dict__[attribute].load_data(data_dict)


class Pipe(StationObject):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = 0
        self.parallels = 1

    def get_re(self, flow, unit):
        diameter = self.diameter.value
        speed = 1000 * self.speed(flow, unit)
        re = (diameter * speed) / self.kinematic_viscosity
        # log.info('Reynolds number is {}'.format(re))
        return re

    def get_epsilon(self):
        diameter = self.diameter.value
        epsilon = self.roughness.value / diameter
        return epsilon

    def get_lambda(self, flow, unit):
        diameter = self.diameter.value * 0.001
        epsilon = self.get_epsilon()
        log.info('Epsilon is {}'.format(epsilon))
        lambda_ = (-2 * np.log10(self.roughness.value / (
            3.71 * diameter))) ** -2
        re = self.get_re(flow, unit)
        # log.info('Re is {}'.format(re))
        # log.info('Lambda is {}'.format(lambda_))
        try:
            alt_lambda = (-2 * np.log10((6.1 / (re ** 0.915)) + (
                0.268 * epsilon))) ** -2
        except ZeroDivisionError as e:
            log.error(e)
            alt_lambda = 0
        # log.info('Alternative Lambda is {}'.format(alt_lambda))
        return alt_lambda

    def line_loss(self, flow, unit):
        log.debug('Starting counting line loss\n')
        diameter = self.diameter.value * 0.001
        std_grav = 9.81
        lambda_coef = self.get_lambda(flow, unit)
        speed = self.speed(flow, unit)
        # log.info('for diameter {} [m²], lambda {} [-], speed {} [m/s]'.format(
        #     diameter, lambda_coef, speed))
        hydraulic_gradient = (lambda_coef * (speed ** 2)) / (
            diameter * 2 * std_grav)
        # log.info('hydraulic gradient is {} [-]\n'.format(hydraulic_gradient))
        line_loss = self.length.value * hydraulic_gradient
        # log.info('line loss is {} [m]\n'.format(line_loss))
        return line_loss

    def local_loss(self, flow, unit):
        local_loss = ((self.speed(flow, unit) ** 2) / (2 * 9.81)) * sum(
            self.resistance.values)
        # log.info('local loss is {} [m]'.format(local_loss))
        # log.info('Epsilon is {}, Re is {}'.format(
        #     self.get_epsilon(), self.get_re(flow, unit)))
        return local_loss

    def speed(self, flow, unit):
        # log.debug('input flow: {} {}'.format(flow, unit_bracket_dict[unit]))
        if unit == 'liters':
            flow *= .001
        elif unit == 'meters':
            flow /= 3600
        radius = (0.001 * self.diameter.value) / 2
        cross_sec = 3.14 * (radius ** 2)
        speed = flow / cross_sec
        log.info(
            'for flow {} [m3/s], radius {} [m], cross section {} [m2]'.format(
                flow, radius, cross_sec))
        # log.info('speed is {} [m/s]'.format(speed))
        return speed

    def sum_loss(self, flow, unit='liters'):
        return self.line_loss(flow, unit) + self.local_loss(flow, unit)

    def pipe_char_ready(self):
        flag = True
        checklist = [self.length, self.diameter, self.roughness]
        for parameter in checklist:
            log.debug('{} = {}'.format(parameter, parameter.value))
            if parameter.value == 0:
                flag = False
        return flag

    def get_y_coords(self, flows, unit):
        log.debug('Getting pipe y coordinates')
        result = [self.sum_loss(flow, unit) for flow in flows]
        log.debug('Pipe loss coords: {}'.format(result))
        return result

    def get_pipe_char_vals(self, station, unit):
        log.debug('Starting getting pipe vals')
        flows, _ = station.pump_type.characteristic.get_pump_char_func(unit)
        y_coords = self.get_y_coords(flows, unit)
        log.debug('Got ys')
        pipes_char = []
        for i in range(len(flows)):
            sum_l = y_coords[i]
            log.debug('####################\n\n')
            log.debug('flow: {}, pipe: {}, sum: {}'.format(
                flows[i], y_coords[i], sum_l))
            log.debug('\n####################\n\n')
            pipes_char.append(sum_l)
        y = maths.fit_coords(flows, pipes_char, 2)
        log.debug('Finding ys finished')
        return y


class PumpType(StationObject):
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
        y = maths.fit_coords(flows, lifts, 3)
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
        Qs = maths.fit_coords(lifts, set_flows, 3)
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
        Q = maths.interp(H, Hs, Qs(Hs))
        # log.debug('linspace of Q (Qs) : {}'.format(Qs(Hs)))
        log.debug('Q for {}m is {}'.format(H, Q))
        return Q


class PumpSet():

    def __init__(self, station):
        self.station = station
        # self.well = station.well
        self.n_of_pumps = self.station.number_of_pumps
        self.characteristic = station.pump_type.characteristic
<<<<<<< HEAD
        # self.set_start_ordinates()
=======
        self.cycle_time = station.pump_type.cycle_time
        self.qp = station.qp
        self.set_start_ordinates()
>>>>>>> 91e599add284f764b6373d33b35d15b0f77070cf
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

    '''
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

    def get_parameters(self, n_of_starting_pump):
        r = ''
        if n_of_starting_pump <= self.n_of_pumps:
            r += 'Parametry poczatkowe pracy zespolu pomp\n'
            r += 'w chwili wlaczenia pompy nr{}\n\n'.format(n_of_starting_pump)
        else:
            r += 'Parametry końcowe pracy zespolu pomp\n\n'
        r += '-wys. lc. u wylotu pompy...........Hlc= {} [m]\n'.format('x')
        r += '-geometryczna wys. podnoszenia.......H= {} [m]\n'.format('x')
        r += '-wydatek.............................Q= {} [l/s]\n'.format('x')
        r += '-predkosc w kolektorze tlocznym......v= {} [m/s]\n'.format('x')
        r += '-predkosc w przewodach w pompowni....v= {} [m/s]\n'.format('x')
        if n_of_starting_pump <= self.n_of_pumps:
            r += ('-zapas wysokosci cisnienia..........dh= '
                  '{} [m sł.wody]\n\n'.format('x'))
        return r
    '''

    def get_pumpset_vals(self):
        log.debug('Starting draw_pipes_plot')
        unit = 'liters'
        flows, lifts = self.characteristic.get_pump_char_func(unit)
        n = self.n_of_pumps
        set_flows = [i * n for i in flows]
        y = maths.fit_coords(set_flows, lifts, 3)
        return y


class Pump():

    def __init__(self, station, pump_set, number):
        self.station = station
        self.well = station.well
        self.pump_set = pump_set
        self.pump_type = station.pump_type
        self.time_to_beat = self.pump_type.cycle_time.value * 60
        self.number = number
        self.ord_start = None
        self.ord_full_stop = self.station.ord_sw_off
        self.ord_pump_lowest = None
        self.real_t_work = 0
        self.real_t_stop = 0
        self.real_T = 0
        self.velo_useful = 0
        self.calc_params()
        log.debug('CALCULATING PARAMS COMPLETED')
        self.report = self.get_work_parameters()
        log.debug(self.report)

    def get_ord_to_iterate(self):
        if self.number == 1:
            return self.station.ord_sw_off
        elif self.number > 1:
            print(type(self.pump_set))
            log.debug('trying to get start ordinate index {}'.format(
                self.number - 1))
            return self.pump_set.start_ords[self.number - 2]
        else:
            log.error('Pump number < 1')
            ##############
            # RAISE EXCEPTION ?
            ##############
            return None

    def get_start_ordinate(self):
        return self.ord_start

    def calc_params(self):
        self.ord_start = self.get_ord_to_iterate()
        self.ord_pump_lowest = self.get_ord_to_iterate()
        self.Q_off, self.H_off = self.get_real_Q_H(self.ord_full_stop)
        step = 0
        while self.real_T < self.time_to_beat:
            step += 1
            self.ord_start += 0.01
            self.velo_useful = self.update_velo_useful()
            self.Q_on, self.H_on = self.get_real_Q_H(self.ord_start)
            self.Q_av = (self.Q_off + self.Q_on) / 2
            self.Q_in = self.get_Q_in()
            self.real_t_stop = self.velo_useful / self.Q_in
            self.real_t_work = self.velo_useful / (self.Q_av - self.Q_in)
            self.real_T = self.real_t_stop + self.real_t_work
            log.info('pump nr {}'.format(self.number))
            log.info('step{}, minT: {}, calcT: {}'.format(
                step, self.time_to_beat, self.real_T))
            log.info('stop time: {}s, run time: {}s'.format(
                self.real_t_stop, self.real_t_work))
            log.info('checking ord to start: {}, all stop at: {}'.format(
                self.ord_start, self.ord_pump_lowest))
            log.info('Velocity useful = {}'.format(self.velo_useful))
            log.info('got Q_off={}, H_off={}, H_geom={}'.format(
                self.Q_off, self.H_off,
                self.station.ord_upper_level.value - self.ord_full_stop))
            log.info('got Q_on={}, H_on={}, Hgeom={}'.format(
                self.Q_on, self.H_on,
                self.station.ord_upper_level.value - self.ord_start))
            log.info('Worst case: {}, Inflow: {}'.format(self.Q_av, self.Q_in))
            log.info('')

    def update_velo_useful(self):
        return 1000 * self.well.cross_sectional_area() * (
            self.ord_start - self.ord_pump_lowest)

    def get_Q_in(self):
        return max((self.Q_av / 2), self.station.inflow_min.value_liters)

    def get_real_Q_H(self, ordinate):
        DIFF = 3
        H = self.station.ord_upper_level.value - ordinate
        step = 0
        difference = 5
        Hs, Qs = self.pump_type.get_Q_for_H(self.number)
        while difference > DIFF:
            step += 1
            Q1 = self.pump_type.get_Q(H, Hs, Qs)
            H = self.station.collector.sum_loss(
                Q1) + self.station.d_pipe.sum_loss(Q1) + H
            Q2 = self.pump_type.get_Q(H, Hs, Qs)
            difference = abs(Q2 - Q1)
            log.debug('finding Q loop')
            log.debug('step{}: Q1: {}, Q2: {}, diff: {}'.format(
                step, Q1, Q2, difference))
        return Q2, H

    def get_work_parameters(self):
        report = ''
        report += 'PARAMETR POMPY NR: {}\n\n'.format(self.number)
        report += 'Rzeczywisty czas cyklu pompy.........T= {} [s]\n'.format(
            self.real_T)
        report += 'Rzeczywisty czas postoju pompy......Tp= {} [s]\n'.format(
            self.real_t_stop)
        report += 'Rzeczywisty czas pracy pompy........Tr= {} [s]\n'.format(
            self.real_t_work)
        report += 'Obj. uzyt. wyzn. przez pompe........Vu= {} [m3]\n'.format(
            self.velo_useful)
        report += 'Rzedna wlaczenia pompy................  {} [m]\n\n'.format(
            self.ord_start)
        report += 'Parametry poczatkowe pracy zespolu pomp\n'
        report += 'w chwili wlaczenia pompy nr {}\n\n'.format(self.number)
        report += '-wys. lc. u wylotu pompy.........Hlc={} [m]\n'.format(
            self.H_on)
        report += '-geometryczna wys. podnoszenia.....H= {} [m]\n'.format(
            self.station.ord_upper_level.value - self.ord_start)
        report += '-wydatek...........................Q= {} [l/s]\n'.format(
            self.Q_on)
        report += '-predkosc w kolektorze tlocznym....v= {} [m/s]\n'.format(
            self.station.collector.speed(self.Q_on, 'liters'))
        report += '-predkosc w przewodach w pompowni..v= {} [m/s]\n'.format(
            self.station.d_pipe.speed(self.Q_on, 'liters'))
        report += '-zapas wysokosci cisnienia.....dh= {} [m sl.wody]\n\n'.format(
            '?')
        report += 'Parametry koncowe pracy zespolu pomp\n\n'
        report += '-wys. lc. u wylotu pompy.........Hlc= {} [m]\n'.format(
            self.H_off)
        report += '-geometryczna wys. podnoszenia.....H= {} [m]\n'.format(
            self.station.ord_upper_level.value - self.ord_full_stop)
        report += '-wydatek...........................Q= {} [l/s]\n'.format(
            self.Q_off)
        report += '-predkosc w kolektorze tlocznym....v= {} [m/s]\n'.format(
            self.station.collector.speed(self.Q_off, 'liters'))
        report += '-predkosc w przewodach w pompowni..v= {} [m/s]\n'.format(
            self.station.d_pipe.speed(self.Q_off, 'liters'))
        report += '-doplyw najniekorzystniejszy....Qdop= {} [l/s]\n'.format(
            self.Q_av)
        report += 'Zakres pracy pomp /maksymalna sprawnosc/\n'
        report += 'Q1= {} [l/s]    Q2= {} [l/s]\n'.format(
            self.pump_type.efficiency_from.value_liters * self.number,
            self.pump_type.efficiency_to.value_liters * self.number)
        return report


class Well(StationObject):
    """class for well"""

    def __init__(self, app):
        super().__init__(app)

        self.pump_type = None
        self.discharge_pipe = None
        self.collector = None

        self.reserve_pumps = None
        self.shape = None
        self.config = None
        # self.set_shape(self.default['shape'])
        self.diameter = 0
        self.length = 0
        self.width = 0

    def set_shape(self, shape):
        self.ui_vars.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = self.builder.get_object('Entry_Well_diameter')
        length = self.builder.get_object('Entry_Well_length')
        width = self.builder.get_object('Entry_Well_width')
        if shape == 'round':
            diameter.configure(state='normal')
            length.configure(state='disabled')
            width.configure(state='disabled')
        elif shape == 'rectangle':
            diameter.configure(state='disabled')
            length.configure(state='normal')
            width.configure(state='normal')
        log.debug('changed shape to {}'.format(shape))

    def minimal_diameter(self, n_work_pumps, n_reserve_pumps, station):
        d = station.pump_type.contour.value
        n = n_work_pumps + n_reserve_pumps
        if self.shape.value == 'round':
            if self.config.value == 'optimal':
                minimal_d = d + 0.6 + 2 * \
                    ((d + 0.6) / (2 * (np.sin(3.14 / n))))
            elif self.config.value == 'singlerow':
                minimal_d = (n * d) + 0.6
        elif self.shape.value == 'rectangle':
            if self.config.value == 'optimal':
                length, width = self.length.value, self.width.value
                short_side = min(length, width)
                rows = short_side // (d + 0.6)
                if n % rows == 0:
                    pumps_in_row = n / rows
                else:
                    pumps_in_row = (n // rows) + 1
                min_len = pumps_in_row * (d + 0.6)
                min_wid = rows * (d + 0.6)
            elif self.config.value == 'singlerow':
                min_len = n * (d + 0.6)
                min_wid = d + 0.6
            minimal_d = 2 * ((min_len * min_wid / 3.14) ** (1 / 2))
        return minimal_d

    def cross_sectional_area(self):
        if self.shape.value == 'rectangle':
            log.debug('rectangle')
            area = self.length.value * self.width.value
            log.debug('len: {}, wid: {}'.format(
                self.length.value, self.width.value))
        elif self.shape.value == 'round':
            log.debug('round')
            log.debug('diameter value: {}'.format(self.diameter.value))
            area = 3.14 * ((self.diameter.value / 2) ** 2)
        log.debug('cross section area is {}'.format(area))
        return area
