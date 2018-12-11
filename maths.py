import logging
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

log = logging.getLogger('Pompa.maths')

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


def init_figure(container, dim_x, dim_y):
    fig = Figure(figsize=(dim_x, dim_y), dpi=100)
    plot = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=container)
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


def draw_plot(x_samples, y_samples, style, unit):

    return x, y(x), style


def draw_report_figure(builder, plot, canvas, station):
    log.debug('Starting draw report figure')
    plot.clear()
    canvas.draw()
    ui_vars = builder.tkvariables
    unit = ui_vars.__getitem__('pump_flow_unit').get()
    x = station.get_x_axis(unit)
    if station.pump_type.pump_char_ready():
        x, y_pump, l_pump = station.pump_type.draw_pump_plot(x)
        plot.plot(x, y_pump, l_pump, label='char. pompy')
    if station.pipes_ready():
        log.debug('Trying to drawing pipes plot')
        x, y_pipe, l_pipe = station.draw_pipes_plot(x, unit)
        log.debug('x: {}, y: {}, look: {}'.format(x, y_pipe, l_pipe))
        plot.plot(
            x, y_pipe, l_pipe, label='char. przewodów')
    if station.pump_type.pump_char_ready() and station.pipes_ready():
        try:
            intersection_f = work_point(y_pump, y_pipe)
            plot.plot(x[intersection_f], y_pump[intersection_f], 'ro',
                      label='punkt pracy')
            str_work_p = str(round(x[intersection_f][0], 2))
        except IndexError as e:
            log.error('ERROR1: {}'.format(e))
            pass
    else:
        str_work_p = ''
    str_unit = unit_bracket_dict[ui_vars.__getitem__(
        'pump_flow_unit').get()]
    plot.set_xlabel(
        'Przepływ Q {}'.format(str_unit))
    plot.set_ylabel('Ciśnienie [m. sł. c.]')
    try:
        if len(x[intersection_f]) == 1:
            plot.set_title('Punkt pracy pompy: {} {}'.format(
                str_work_p, str_unit))
        elif len(x[intersection_f]) > 1:
            list_points = [np.around(val, 2)
                           for val in x[intersection_f]]
            plot.set_title('Punkty pracy pompy: {} {}'.format(
                list_points, str_unit))
    except UnboundLocalError:
        plot.set_title('Punkt pracy pompy: {} {}'.format(
            str_work_p, str_unit), fontsize='small')
        pass
    if unit == 'meters':
        plot.xaxis.set_minor_locator(MultipleLocator(5))
    elif unit == 'liters':
        plot.xaxis.set_minor_locator(MultipleLocator(2))
    plot.yaxis.set_minor_locator(MultipleLocator(1))
    plot.grid(True, 'minor', linestyle='--', linewidth=.3)
    plot.grid(True, 'major', linestyle='--')
    try:
        eff_from_x = station.pump_type.efficiency_from.value
        eff_from_y = interp(eff_from_x, x, y_pump)
        eff_to_x = station.pump_type.efficiency_to.value
        eff_to_y = interp(eff_to_x, x, y_pump)
        plot.plot([eff_from_x, eff_from_x], [-100, eff_from_y], 'r--')
        plot.plot([eff_to_x, eff_to_x], [-100, eff_to_y], 'r--',
                  label='maks. wydajność pompy')
        work_p_x = x[intersection_f]
        log.info('work_p_x: {}'.format(work_p_x))
        work_p_y = [interp(i, x, y_pump) for i in work_p_x]
        for i in range(len(work_p_x)):
            plot.plot([work_p_x[i], work_p_x[i]],
                      [-100, work_p_y[i]], color='black',
                      linewidth=.8)
    except UnboundLocalError as e:
        log.error('Unbound ERROR2: {}'.format(e))
        pass
    plot.set_xlim(left=x[0], right=x[-1])
    plot.set_ylim(bottom=0)
    plot.legend(fontsize='small')
    canvas.draw()


def draw_pipe_figure(builder, plot, canvas, station):
    log.debug('Starting draw report figure')
    plot.clear()
    canvas.draw()
    ui_vars = builder.tkvariables
    unit = ui_vars.__getitem__('inflow_unit').get()
    x = station.get_x_axis(unit)
    if station.d_pipe.pipe_char_ready():
        pass
    if station.collector.pipe_char_ready():
        pass


def draw_pump_figure():
    pass


def draw_schema():
    pass
