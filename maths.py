import logging
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

log = logging.getLogger('Pompa.maths')


def init_figures(fcontainer):
    fig = Figure(figsize=(4.2, 5.1), dpi=100)
    plot = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=fcontainer)
    return fig, plot, canvas


def fit_coords(xcoords, ycoords, degree):
    log.debug('x: {}, y:{}'.format(xcoords, ycoords))
    x = np.array(xcoords)
    y = np.array(ycoords)
    log.debug('arr x: {}, arr y:{}'.format(x, y))
    polyf = np.polyfit(x, y, degree)
    fitted_y = np.poly1d(polyf)
    log.debug('arr x: {}, fit y:{}'.format(x, fitted_y))
    return fitted_y


def work_point(pump, pipes):
    return np.argwhere(np.diff(np.sign(pump - pipes))).flatten()


def interp(wanted_x, x_arr, y_arr):
    return np.interp(wanted_x, x_arr, y_arr)
