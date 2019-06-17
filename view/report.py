import logging
log = logging.getLogger('pompa.report')


class Report():

    # UWAGA - Do uzupełnienia argument dla minimalnej średnicy pompowni

    def __init__(self, station):
        self.station = station
        self.content = {}
        self.content['1'] = 'POMPA   POMPA   POMPA   POMPA   POMPA   ' +\
            'POMPA   POMPA\n\n'
        self.content['2'] = self.write_conf(station.well.config.value)
        self.content['3'] = 'Liczba dobranych pomp roboczych .....n= ' +\
            '{} szt.'.format(station.n_of_pumps)
        self.content['4'] = 'Liczba pomp rezerwowych.............nr= ' +\
            '{} szt.'.format(station.n_of_res_pumps)
        self.content['5'] = 'Srednica kola opisujacego pompe.....Dn= ' +\
            '{} [m]'.format(station.pump.contour.value)
        self.content['6'] = 'Srednica pompowni...................DN= ' +\
            '{} [m]'.format(station.well.diameter.value)
        self.content['7'] = 'Minimalna srednica pompowni......DNmin= ' +\
            '{} [m]'.format("%0.2f" % station.well.minimal_diameter(
                station.n_of_pumps + station.n_of_res_pumps, station))
        self.content['8'] = 'Pole poziomego przekroju pompowni....F= ' +\
            '{} [m2]'.format(station.well.area)
        self.content['9'] = 'Ilosc przewodow tlocznych (kolektor)... ' +\
            '{} szt.'.format(station.out_pipe.parallels.value)
        self.content['10'] = 'Dlugosc kolektora tlocznego..........L= ' +\
            '{} [m]'.format(station.out_pipe.length.value)
        self.content['11'] = 'Dlugosc przewodu w pompowni..........L= ' +\
            '{} [m]'.format(station.ins_pipe.length.value)
        self.content['12'] = 'Srednica kolektora tlocznego........Dn= ' +\
            '{} [mm]'.format(station.out_pipe.diameter.value)
        self.content['13'] = 'Srednica przewodu w pompowni........Dn= ' +\
            '{} [mm]'.format(station.ins_pipe.diameter.value)
        self.content['14'] = 'Chropowatosc kolektora tlocznego.....k= ' +\
            '{} [mm]'.format(station.out_pipe.roughness.value)
        self.content['15'] = 'Chropowatosc przewodu w pompowni.....k= ' +\
            '{} [mm]'.format(station.ins_pipe.roughness.value)
        self.content['16'] = 'Doplyw do pomowni....Qmin= {}   Qmax= {}' +\
            ' [l/s]'.format(station.inflow_min.v_lps, station.inflow_max.v_lps)
        self.content['17'] = 'Rzedna terenu.........................  ' +\
            '{} [m]'.format(station.ord_terrain.value)
        self.content['18'] = 'Rzedna doplywu sciekow................  ' +\
            '{} [m]'.format(station.ord_inlet.value)
        self.content['19'] = 'Rzedna wylotu sciekow /przejscie'
        self.content['21'] = 'osi rury przez sciane pompowni/.......  ' +\
            '{} [m]'.format(station.ord_outlet.value)
        self.content['22'] = 'Rzedna najwyzszego pkt. na trasie.....  ' +\
            '{} [m]'.format(station.ord_highest_point.value)
        self.content['23'] = 'Rzedna zwierciadla w zbiorniku górnym.  ' +\
            '{} [m]'.format(station.ord_upper_level.value)
        self.content['24'] = 'Min. wysokosc sciekow w  pompowni.....  ' +\
            '{} [m]'.format(station.minimal_sewage_level.value)
        self.content['25'] = 'Suma wsp. oporow miejsc. kolektora....  ' +\
            '{} [-]'.format(sum(station.out_pipe.resistance.values))
        self.content['26'] = 'Suma wsp. oporow miejsc. w pompowni...  ' +\
            '{} [-]\n'.format(sum(station.ins_pipe.resistance.values))
        self.content['27'] = 'CHARAKTERYSTYKA ZASTOSOWANYCH POMP\n'
        self.content['30'] = self.station.pump.generate_pump_char_string()
        self.content['31'] = 'Rzedna dna pompowni...................  ' +\
            '{}\t[m]'.format("%0.2f" % station.ord_bottom.value)
        self.content['32'] = 'Rzedna wylaczenia sie pomp............  ' +\
            '{}\t[m]'.format("%0.2f" % station.ord_sw_off)
        self.content['33'] = 'Objetosc calkowita pompowni.........Vc= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_whole)
        self.content['34'] = 'Objetosc uzyteczna pompowni.........Vu= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_useful)
        self.content['35'] = 'Objetosc rezerwowa pompowni.........Vr= ' +\
            '{}\t[m3]'.format("%0.2f" % station.v_reserve)
        self.content['36'] = 'Objetosc martwa pompowni............Vm= ' +\
            '{}\t[m3]\n'.format("%0.2f" % station.v_dead)
        self.content['37'] = 'Vu/Vc = {}%'.format("%0.2f" % (100 * (
            station.v_useful / station.v_whole)))
        self.content['38'] = 'Vr/Vu = {}%'.format("%0.2f" % (100 * (
            station.v_reserve / station.v_useful)))
        self.content['39'] = 'Vr/Vc = {}%'.format("%0.2f" % (100 * (
            station.v_reserve / station.v_whole)))
        self.content['40'] = 'Vm/Vc = {}%\n'.format("%0.2f" % (100 * (
            station.v_dead / station.v_whole)))

        self.content['41'] = self.pump_report()

        self.print_rep()

    def write_conf(self, config):
        conf_dict = {'singlerow': 'Liniowe',
                     'optimal': 'Optymalne'}
        log.debug('config: {}'.format(config))
        log.debug('confdict[config]: {}'.format(conf_dict[config]))
        return '{} ustawienie pomp w pompowni'.format(conf_dict[config])

    def convert_to_string(self):
        string_report = ''
        for i in self.content:
            log.debug('line {}: {}'.format(i, self.content[i]))
            if self.content[i] is not None:
                string_report += self.content[i]
                string_report += '\n'
        return string_report

    def print_rep(self):
        self.string = self.convert_to_string()
        print(self.string)

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
            report += 'Obj. uzyt. wyzn. przez pompe......Vu= ' +\
                '{}\t[m3]\n'.format("%0.2f" % prms['vol_a'])
            report += 'Rzedna wlaczenia pompy..............  ' +\
                '{}\t[m]\n\n'.format("%0.2f" % prms['ord_sw_on'])
            report += 'Parametry poczatkowe pracy zespolu pomp\n' +\
                'w chwili wlaczenia pompy nr{}\n\n'.format(pump_no)
            report += '-wys. lc. u wylotu pompy.........Hlc= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['start'][0])
            report += '-geometryczna wys. podnoszenia.....H= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['start'][1])
            report += '-wydatek...........................Q= ' +\
                '{}\t[l/s]\n'.format("%0.2f" % prms['start'][2].v_lps)
            report += '-predkosc w kolektorze tlocznym....v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['start'][3])
            report += '-predkosc w przewodach w pompowni..v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['start'][4])
            """
            USUNIĘTO PO ROZMOWIE Z DRem WAYSEM
            report += '-zapas wysokosci cisnienia.....dh=  {}
            \t[m sl.wody]\n\n'.format('??')
            """
            report += 'Parametry koncowe pracy zespolu pomp\n\n'
            report += '-wys. lc. u wylotu pompy.........Hlc= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['stop'][0])
            report += '-geometryczna wys. podnoszenia.....H= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['stop'][1])
            report += '-wydatek...........................Q= ' +\
                '{}\t[l/s]\n'.format("%0.2f" % prms['stop'][2].v_lps)
            report += '-predkosc w kolektorze tlocznym....v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['stop'][3])
            report += '-predkosc w przewodach w pompowni..v= ' +\
                '{}\t[m/s]\n'.format("%0.2f" % prms['stop'][4])
            report += '-doplyw najniekorzystniejszy....Qdop= ' +\
                '{}\t[m]\n'.format("%0.2f" % prms['worst_infl'].v_lps)
            report += 'Zakres pracy pomp /maksymalna sprawnosc/\n'
            report += 'Q1=  {} [l/s]    Q2=  {} [l/s]\n'.format(
                (pump_no) * self.station.pump.efficiency_from.v_lps,
                (pump_no) * self.station.pump.efficiency_to.v_lps)
            report += '\n\n'

        report += '\n\n'
        return report
