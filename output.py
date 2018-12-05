import hydraulics


def generate_checking_report(well):
    pump = well.pump
    dpipe = well.discharge_pipe
    coll = well.collector

    n_of_work_pumps = well.number_of_pumps()
    n_of_res_pumps = well.reserve_pumps_number()

    report = {}

    report['1'] = 'POMPA   POMPA   POMPA   POMPA   POMPA   POMPA   POMPA\n\n'
    report['2'] = 'Liniowe ustawienie pomp w pompowni'  # słownik
    report['3'] = 'Liczba dobranych pomp roboczych .....n= {} szt.'.format(
        n_of_work_pumps)
    report['3'] = 'Liczba pomp rezerwowych.............nr= {} szt.'.format(
        n_of_res_pumps)
    report['4'] = 'Srednica kola opisujacego pompe.....Dn= {} [m]'.format(
        pump.contour.value)
    report['5'] = 'Srednica pompowni...................DN= {} [m]'.format(
        well.diameter.value)
    report['6'] = 'Minimalna srednica pompowni......DNmin= {} [m]'.format(
        well.minimal_diameter())
    report['7'] = 'Pole poziomego przekroju pompowni....F= {} [m2]'.format(
        well.cross_sectional_area())
    report['8'] = 'Ilosc przewodow tlocznych (kolektor)... {} szt.'.format(
        coll.parallels.value)
    report['9'] = 'Dlugosc kolektora tlocznego..........L= {} [m]'.format(
        coll.length.value)
    report['10'] = 'Dlugosc przewodu w pompowni..........L= {} [m]'.format(
        dpipe.length.value)
    report['11'] = 'Srednica kolektora tlocznego........Dn= {} [mm]'.format(
        coll.diameter.value)
    report['12'] = 'Srednica przewodu w pompowni........Dn= {} [mm]'.format(
        dpipe.diameter.value)
    report['13'] = 'Chropowatosc kolektora tlocznego.....k= {} [mm]'.format(
        coll.roughness.value)
    report['14'] = 'Chropowatosc przewodu w pompowni.....k= {} [mm]'.format(
        dpipe.roughness.value)
    report['15'] = 'Doplyw do pomowni...Qmin=  {}   Qmax=  {}  [l/s]'.format(
        well.inflow_min.value_liters, well.inflow_max.value_liters)
    report['16'] = 'Rzedna terenu.........................  {} [m]'.format(
        well.ord_terrain.value)
    report['17'] = 'Rzedna doplywu sciekow................  {} [m]'.format(
        well.ord_inlet.value)
    report['18'] = 'Rzedna wylotu sciekow /przejscie'
    report['19'] = 'osi rury przez sciane pompowni/.......  {} [m]'.format(
        well.ord_outlet.value)
    report['20'] = 'Rzedna najwyzszego pkt. na trasie.....  {} [m]'.format(
        well.ord_highest_point.value)
    report['21'] = 'Rzedna zwierciadla w zbiorniku górnym.  {} [m]'.format(
        well.ord_upper_level.value)
    report['22'] = 'Min. wysokosc sciekow w  pompowni.....  {} [m]'.format(
        well.minimal_sewage_level.value)
    report['23'] = 'Suma wsp. oporow miejsc. kolektora....  {} [-]'.format(
        sum(coll.resistance.values))
    report['24'] = 'Suma wsp. oporow miejsc. w pompowni...  {} [-]\n'.format(
        sum(dpipe.resistance.values))
    report['25'] = 'CHARAKTERYSTYKA ZASTOSOWANYCH POMP\n'
    report['30'] = pump.generate_pump_char_string()
    report['31'] = 'Rzedna dna pompowni...................  {} [m]'.format(
        well.ord_bottom.value)
    report['32'] = 'Rzedna wylaczenia sie pomp............  {} [m]'.format(
        well.ord_bottom + 0.3)
    report['33'] = 'Objetosc calkowita pompowni.........Vc= {} [m3]'.format(
        well.velocity_whole())
    report['34'] = 'Objetosc uzyteczna pompowni.........Vu= {} [m3]'.format(
        well.velocity_useful())
    report['35'] = 'Objetosc rezerwowa pompowni.........Vr= {} [m3]'.format(
        well.velocity_reserve())
    report['36'] = 'Objetosc martwa pompowni............Vm= {} [m3]\n'.format(
        well.velocity_dead())
    report['37'] = 'Vu/Vc = {}%'.format(
        well.velocity_useful() / well.velocity_whole())
    report['38'] = 'Vr/Vu = *****  %'
    report['39'] = 'Vr/Vc = {}%'.format(
        well.velocity_reserve() / well.velocity_whole())
    report['40'] = 'Vm/Vc = {}%\n'.format(
        well.velocity_dead() / well.velocity_whole())
    report['41'] = well.pump_set_report(n_of_work_pumps)
    '''
    report['41'] = 'PARAMETRY POMPY NR: {}\n'.format()
    report['42'] = 'Rzeczywisty czas cyklu pompy.........T= {} [s]'.format()
    report['43'] = 'Rzeczywisty czas postoju pompy......Tp= {} [s]'.format()
    report['44'] = 'Rzeczywisty czas pracy pompy........Tr= {} [s]'.format()
    report['45'] = 'Obj. uzyt. wyzn. przez pompe........Vu= {} [m3]'.format()
    report['46'] = 'Rzedna wlaczenia pompy................  {} [m]\n'.format()
    report['47'] = 'Parametry poczatkowe pracy zespolu pomp'
    report['48'] = 'w chwili wlaczenia pompy nr{}\n'.format()
    report['49'] = '-wys. lc. u wylotu pompy...........Hlc= {} [m]'.format()
    report['50'] = '-geometryczna wys. podnoszenia.......H= {} [m]'.format()
    report['51'] = '-wydatek.............................Q= {} [l/s]'.format()
    report['52'] = '-predkosc w kolektorze tlocznym......v= {} [m/s]'.format()
    report['53'] = '-predkosc w przewodach w pompowni....v= {} [m/s]'.format()
    report['54'] = '-zapas wysokosci cisnienia..........dh= {} [m sł.wody]\n'.format()
    report['55'] = 'Parametry koncowe pracy zespolu pomp\n'
    report['56'] = '-wys. lc. u wylotu pompy...........Hlc= {} [m]'.format()
    report['57'] = '-geometryczna wys. podnoszenia.......H= {} [m]'.format()
    report['58'] = '-wydatek.............................Q= {} [l/s]'.format()
    report['59'] = '-predkosc w kolektorze tlocznym......v= {} [m/s]'.format()
    report['60'] = '-predkosc w przewodach w pompowni....v= {} [m/s]'.format()
    report['61'] = '-doplyw najniekorzystniejszy....Qdop=   {} [l/s]'.format()
    report['62'] = 'Zakres pracy pomp /maksymalna sprawnosc/'
    report['63'] = 'Q1= {} [l/s]    Q2= {} [l/s]'.format()
    '''

    return report
