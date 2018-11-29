import logging
import numpy as np

log = logging.getLogger('Pompa/main.maths')


def fit_coords(xcoords, ycoords):
    log.debug('x: {}, y:{}'.format(xcoords, ycoords))
    x = np.array(xcoords)
    y = np.array(ycoords)
    # degree = len(xcoords) - 1
    log.debug('arr x: {}, arr y:{}'.format(x, y))
    polyf = np.polyfit(x, y, 5)
    fitted_y = np.poly1d(polyf)
    log.debug('arr x: {}, fit y:{}'.format(x, fitted_y))
    specified_x = np.linspace(xcoords[0], xcoords[-1], 100)
    return specified_x, fitted_y
