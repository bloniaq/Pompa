import logging
import numpy as np

log = logging.getLogger('Pompa.calcs')

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


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
    xcoords.sort()
    for value in xcoords:
        ycoords.append(pairs[str(value)])
    x = np.array(xcoords)
    y = np.array(ycoords)
    return x, y


def work_point(pump, pipes):
    return np.argwhere(np.diff(np.sign(pump - pipes))).flatten()


def interp(wanted_x, x_arr, y_arr):
    return np.interp(wanted_x, x_arr, y_arr)
