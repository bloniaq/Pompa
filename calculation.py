import logging
import numpy as np

log = logging.getLogger('Pompa.calcs')

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


def work_point(pump, pipes):
    return np.argwhere(np.diff(np.sign(pump - pipes))).flatten()


def interp(wanted_x, x_arr, y_arr):
    return np.interp(wanted_x, x_arr, y_arr)


def get_x_axis(station, unit, n=1):
    """returns horizontal array of figures
    """
    log.debug("station: {}\ntype: {}".format(station, type(station)))
    inflow_val_min = station.inflow_min.ret_unit(unit)
    inflow_val_max = station.inflow_max.ret_unit(unit)
    eff_from = station.pump.efficiency_from.ret_unit(unit)
    eff_to = station.pump.efficiency_to.ret_unit(unit)
    x_min = min(inflow_val_min - 3, eff_from - 3)
    if x_min < 0:
        x_min = 0
    x_max = max(1.5 * (inflow_val_max + 3), 1.5 * (eff_to + 3),
                n * (inflow_val_max + 3))
    return np.linspace(x_min, x_max, 200)


def fit_coords(xcoords, ycoords, degree):
    log.error('x: {}, y:{}'.format(xcoords, ycoords))
    x, y = sort_by_x(xcoords, ycoords)
    log.error('arr x: {}, arr y:{}'.format(x, y))
    for i in x:
        log.error('type {}: {}'.format(i, type(i)))
        i = i.value_liters
        log.error('type {}: {}'.format(i, type(i)))
    for j in y:
        log.error('type {}: {}'.format(j, type(j)))
    for k in x:
        log.error('type {}: {}'.format(k, type(j)))
    polyf = np.polyfit(x, y, degree)
    fitted_y = np.poly1d(polyf)
    log.debug('arr x: {}, fit y:{}'.format(x, fitted_y))
    return fitted_y


def sort_by_x(x_list, y_list):
    xcoords = []
    ycoords = []
    pairs = {}
    for i in range(len(x_list)):
        pairs[str(x_list[i])] = y_list[i]
        xcoords.append(x_list[i])
    log.error('x: {}, y:{}'.format(xcoords, ycoords))
    for i in x_list:
        log.error("{}, type: {}".format(i, type(i)))
    for coord in range(len(xcoords)):
        log.error("{} type of {} element: {}".format(coord, xcoords[coord],
                                                     type(xcoords[coord])))

    xcoords.sort()
    x_values = []
    for value in xcoords:
        # x_values.append(value.value_liters)
        ycoords.append(pairs[str(value)])
    x = np.array(xcoords)
    y = np.array(ycoords)
    return x, y


def calc_number_of_pumps(station):
    """Sets number of work pumps, based on min and max inflow, and pump
    efficiency

    TO MAKE TEST THIS FUNCTION!
    """
    log.debug('calc_number_of_pumps START')
    max_pump_eff = station.pump.max_pump_efficiency()
    log.debug('minimal inflow value_liters {}'.format(
        station.inflow_min.value_liters))
    if max_pump_eff.value_liters < station.inflow_min.value_liters:
        log.error('Too low pump efficiency !!!')
        ##############################
        # EXCEPTION TO RAISE !!!
        ##############################
        log.error('Pump has too less efficiency to this station')
        return 0
    number_of_pumps = int(np.ceil((1.1 * station.inflow_max.value_liters) /
                                  max_pump_eff.value_liters))
    log.debug('Result: {}'.format(number_of_pumps))
    station.number_of_pumps = number_of_pumps
    return number_of_pumps


def reserve_pumps_number(station):
    """Sets number of reserve pumps, based on user choose"""
    if station.reserve_pumps.value == 'minimal':
        n_of_res_pumps = 1
    elif station.reserve_pumps.value == 'optimal':
        if station.number_of_pumps % 2 == 0:
            n_of_res_pumps = int(station.number_of_pumps / 2)
        else:
            n_of_res_pumps = int(station.number_of_pumps / 2) + 1
    elif station.reserve_pumps.value == 'safe':
        n_of_res_pumps = station.number_of_pumps
    station.number_of_res_pumps = n_of_res_pumps
    return n_of_res_pumps


def check_get_useful_velo(station):
    useful_velo = ((((
        station.pump.cycle_time.value) * 60) * station.qp) / 4000)
    log.info('useful velo is {}m3'.format(useful_velo))
    return useful_velo
