import logging
import numpy as np

log = logging.getLogger('Pompa.maths')


def fit_coords(xcoords, ycoords, degree):
    log.debug('x: {}, y:{}'.format(xcoords, ycoords))
    x = np.array(xcoords)
    y = np.array(ycoords)
    log.debug('arr x: {}, arr y:{}'.format(x, y))
    polyf = np.polyfit(x, y, degree)
    fitted_y = np.poly1d(polyf)
    log.debug('arr x: {}, fit y:{}'.format(x, fitted_y))
    return fitted_y


def get_x_axis(inflow_min, inflow_max, eff_from, eff_to, unit):
    if unit == 'meters':
        inflow_val_min = inflow_min.value_meters
        inflow_val_max = inflow_max.value_meters
        eff_from = eff_from.value_meters
        eff_to = eff_to.value_meters
    elif unit == 'liters':
        inflow_val_min = inflow_min.value_liters
        inflow_val_max = inflow_max.value_liters
        eff_from = eff_from.value_liters
        eff_to = eff_to.value_liters
    x_min = min(inflow_val_min - 3, eff_from - 3)
    if x_min < 0:
        x_min = 0
    x_max = max(inflow_val_max + 3, eff_to + 3)
    return np.linspace(x_min, 1.5 * x_max, 200)


def work_point(pump, pipes):
    return np.argwhere(np.diff(np.sign(pump - pipes))).flatten()


def log10(x):
    return np.log10(x)


def interp(wanted_x, x_arr, y_arr):
    return np.interp(wanted_x, x_arr, y_arr)
