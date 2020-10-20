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
    log.debug('x: {}, y:{}'.format(xcoords, ycoords))
    x, y = sort_by_x(xcoords, ycoords)
    log.debug('arr x: {}, arr y:{}'.format(x, y))
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

    xcoords.sort()
    # x_values = []
    for value in xcoords:
        # x_values.append(value.value_liters)
        ycoords.append(pairs[str(value)])
    x = np.array(xcoords)
    y = np.array(ycoords)
    return x, y
