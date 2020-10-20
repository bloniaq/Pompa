import logging
log = logging.getLogger('pompa.report')


class Report():

    def __init__(self, station, mode):
        self.station = station
        self.content = {}
        self.content['1'] = 'POMPA   POMPA   POMPA   POMPA   POMPA   ' +\
            'POMPA   POMPA\n'
        self.content['2'] = self.write_statement(station.statement)
        self.content['3'] = self.write_conf(station.well.config.value)
        self.content['4'] = 'Liczba dobranych pomp roboczych .....n= ' +\
            '{} szt.'.format(station.n_of_pumps)
        self.content['5'] = 'Liczba pomp rezerwowych.............nr= ' +\
            '{} szt.'.format(station.n_of_res_pumps)
        self.content['6'] = 'Średnica koła opisującego pompę.....Dn= ' +\
            '{} [m]'.format(station.pump.contour.value)
        self.content['7'] = self.write_dimensions(station.well.shape.value)
        self.content['8'] = self.write_min_dimensions(station.well.shape.value)
        self.content['9'] = 'Pole poziomego przekroju pompowni....F= ' +\
            '{} [m2]'.format(station.well.area)
        self.content['11'] = 'Liczba równoległych przewodów zewn..... ' +\
            '{} szt.'.format(station.out_pipe.parallels.value)
        self.content['12'] = 'Długość pojedynczego przewodu zewn...L= ' +\
            '{} [m]'.format(station.out_pipe.length.value)
        self.content['13'] = 'Długość przewodu wewn. pompowni......L= ' +\
            '{} [m]'.format("%0.2f" % station.ins_pipe.length.value)
        self.content['14'] = 'Średnica pojedynczego przewodu zewn.Dn= ' +\
            '{} [mm]'.format(station.out_pipe.diameter.value)
        self.content['15'] = 'Średnica przewodu wewn. pompowni....Dn= ' +\
            '{} [mm]'.format(station.ins_pipe.diameter.value)
        self.content['16'] = 'Chropowatość przewodu zewn...........k= ' +\
            '{} [mm]'.format(station.out_pipe.roughness.value)
        self.content['17'] = 'Chropowatość przewodu wewn. pompowni.k= ' +\
            '{} [mm]'.format(station.ins_pipe.roughness.value)
        self.content['18'] = 'Dopływ do pompowni....Qmin= ' +\
            '{}   Qmax= {} [l/s]'.format(
                station.inflow_min.v_lps, station.inflow_max.v_lps)
        self.content['19'] = 'Rzędna terenu.........................  ' +\
            '{} [m]'.format(station.ord_terrain.value)
        self.content['21'] = 'Rzędna dopływu ścieków................  ' +\
            '{} [m]'.format(station.ord_inlet.value)
        self.content['22'] = 'Rzędna wylotu scieków /przejście'
        self.content['23'] = 'osi rury przez ścianę pompowni/.......  ' +\
            '{} [m]'.format(station.ord_outlet.value)
        self.content['24'] = 'Rzędna najwyższego pkt. na trasie.....  ' +\
            '{} [m]'.format(station.ord_highest_point.value)
        self.content['25'] = 'Rzędna zwierciadła w zbiorniku górnym.  ' +\
            '{} [m]'.format(station.ord_upper_level.value)
        self.content['26'] = 'Min. wysokość ścieków w pompowni......  ' +\
            '{} [m]'.format(station.minimal_sewage_level.value)
        self.content['27'] = 'Suma wsp. oporów miejsc. przewodu zewn  ' +\
            '{} [-]'.format(sum(station.out_pipe.resistance.values))
        self.content['28'] = 'Suma wsp. oporów miejsc. przewodu wewn  ' +\
            '{} [-]'.format(sum(station.ins_pipe.resistance.values))
        self.content['30'] = '\nCHARAKTERYSTYKA ZASTOSOWANYCH POMP\n'
        self.content['31'] = self.station.pump.generate_pump_char_string()
        self.content['32'] = 'Rzędna dna pompowni...................  ' +\
            '{}\t[m]'.format("%0.2f" % station.ord_bottom.value)
        self.content['33'] = 'Rzędna wyłączenia się pomp............  ' +\
            '{}\t[m]'.format("%0.2f" % station.ord_sw_off)
        self.content['34'] = 'Objętość całkowita pompowni.........Vc= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_whole)
        self.content['35'] = 'Objętość użyteczna pompowni.........Vu= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_useful)
        self.content['36'] = 'Objętość rezerwowa pompowni.........Vr= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_reserve)
        self.content['37'] = 'Objętość martwa pompowni............Vm= ' +\
            '{}\t[m3]\n'.format("%0.2f" % station.v_dead)
        self.content['38'] = 'Vu/Vc = {}%'.format("%0.2f" % (100 * (
            station.v_useful / station.v_whole)))
        self.content['39'] = 'Vr/Vu = {}%'.format("%0.2f" % (100 * (
            station.v_reserve / station.v_useful)))
        self.content['40'] = 'Vr/Vc = {}%'.format("%0.2f" % (100 * (
            station.v_reserve / station.v_whole)))
        self.content['41'] = 'Vm/Vc = {}%\n'.format("%0.2f" % (100 * (
            station.v_dead / station.v_whole)))

        self.content['42'] = self.pump_report()

    def write_statement(self, content):
        if content == '':
            return '\n'
        else:
            return '\n' + content + '\n'

    def write_conf(self, config):
        conf_dict = {'singlerow': 'Liniowe',
                     'optimal': 'Optymalne'}
        log.debug('config: {}'.format(config))
        log.debug('confdict[config]: {}'.format(conf_dict[config]))
        return '{} ustawienie pomp w pompowni'.format(conf_dict[config])

    def write_dimensions(self, shape):
        """ Prepares and returns report text about dimensions of well.
        First it checks shape of well, and then it produce content based on
        proper parameters of well.
        """
        dimension_report = ''
        if shape == 'round':
            dimension_report += 'Średnica pompowni...................DN= '
            dimension_report += '{} [m]'.format(
                "%0.2f" % self.station.well.diameter.value)
        elif shape == 'rectangle':
            dimension_report += 'Długość pompowni.....................L= '
            dimension_report += '{} [m]\n'.format(
                "%0.2f" % self.station.well.length.value)
            dimension_report += 'Szerokość pompowni...................B= '
            dimension_report += '{} [m]'.format(
                "%0.2f" % self.station.well.width.value)
        return dimension_report

    def write_min_dimensions(self, shape):
        """ Prepares and returns report text about minimal dimensions of well.
        First it checks shape of well, and then it produce content based on
        proper parameters of well.
        """
        min_dimension_report = ''
        if shape == 'round':
            min_dimension_report += 'Minimalna średnica pompowni......DNmin= '
            min_dimension_report += '{} [m]'.format(
                "%0.2f" % self.station.well.min_diameter)
        elif shape == 'rectangle':
            min_dimension_report += 'Minimalna dlugość pompowni........Lmin= '
            min_dimension_report += '{} [m]\n'.format(
                "%0.2f" % self.station.well.min_length)
            min_dimension_report += 'Minimalna szerokość pompowni......Bmin= '
            min_dimension_report += '{} [m]'.format(
                "%0.2f" % self.station.well.min_width)
        return min_dimension_report

    def convert_to_string(self):
        string_report = ''
        for i in self.content:
            log.debug('line {}: {}'.format(i, self.content[i]))
            if self.content[i] is not None:
                string_report += self.content[i]
                string_report += '\n'
        return string_report

    def pump_report(self):
        report = ''
        for pump in range(self.station.n_of_pumps):
            pump_no = pump + 1
            prms = self.station.work_parameters[str(pump_no)]
            report += 'PARAMETRY POMPY NR: {}\n\n'.format(pump_no)
            report += 'Rzeczywisty czas cyklu pompy.......T= ' +\
                '{}\t[s]\n'.format("%0.1f" % prms['times'][0])
            report += 'Rzeczywisty czas postoju pompy....Tp= ' +\
                '{}\t[s]\n'.format("%0.1f" % prms['times'][1])
            report += 'Rzeczywisty czas pracy pompy......Tr= ' +\
                '{}\t[s]\n'.format("%0.1f" % prms['times'][2])
            report += 'Obj. użyt. wyzn. przez pompę......Vu= ' +\
                '{}\t[m3]\n'.format("%0.2f" % prms['vol_a'])
            report += 'Rzędna włączenia pompy..............  ' +\
                '{}\t[m]\n\n'.format("%0.2f" % prms['ord_sw_on'])
            report += 'Parametry początkowe pracy zespołu pomp\n' +\
                'w chwili włączenia pompy nr{}\n\n'.format(pump_no)
            report += '-wys. lc. u wylotu pompy.........Hlc= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['start'][0])
            report += '-geometryczna wys. podnoszenia.....H= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['start'][1])
            report += '-wydatek...........................Q= ' +\
                '{}\t[l/s]\n'.format("%0.2f" % prms['start'][2].v_lps)
            report += '-predkość w przewodzie zewn........v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['start'][3])
            report += '-predkość w przewodzie wewn........v= ' +\
                '{}\t[m/s]\n\n'.format("%0.2f" % prms['start'][4])
            """
            USUNIĘTO PO ROZMOWIE Z DRem WAYSEM
            report += '-zapas wysokosci cisnienia.....dh=  {}
            \t[m sl.wody]\n\n'.format('??')
            """
            report += 'Parametry końcowe pracy zespołu pomp\n\n'
            report += '-wys. lc. u wylotu pompy.........Hlc= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['stop'][0])
            report += '-geometryczna wys. podnoszenia.....H= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['stop'][1])
            report += '-wydatek...........................Q= ' +\
                '{}\t[l/s]\n'.format("%0.2f" % prms['stop'][2].v_lps)
            report += '-predkość w przewodzie zewn........v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['stop'][3])
            report += '-predkość w przewodzie wewn........v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['stop'][4])
            report += '-dopływ najniekorzystniejszy....Qdop= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['worst_infl'].v_lps)
            report += 'Zakres pracy pomp /maksymalna sprawność/\n'
            report += 'Q1=  {} [l/s]    Q2=  {} [l/s]\n'.format(
                (pump_no) * self.station.pump.efficiency_from.v_lps,
                (pump_no) * self.station.pump.efficiency_to.v_lps)
            report += '\n\n'

        report += '\n\n'
        return report
