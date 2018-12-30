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


def set_plot_grids(plot, unit):
    if unit == 'meters':
        plot.xaxis.set_minor_locator(MultipleLocator(5))
    elif unit == 'liters':
        plot.xaxis.set_minor_locator(MultipleLocator(2))
    plot.yaxis.set_minor_locator(MultipleLocator(1))
    plot.grid(True, 'minor', linestyle='--', linewidth=.3)
    plot.grid(True, 'major', linestyle='--')


def draw_report_figure(builder, plot, canvas, station):
    log.debug('Starting draw report figure')
    plot.clear()
    canvas.draw()
    ui_vars = builder.tkvariables
    unit = ui_vars.__getitem__('pump_flow_unit').get()
    n = station.number_of_pumps
    x = station.get_x_axis(unit, n)
    if station.pump_type.pump_char_ready():
        l_pump = 'b-'
        y_pump = station.pump_type.draw_pump_plot()
        plot.plot(x, y_pump(x), l_pump, label='char. jednej pompy')
    if station.pipes_ready():
        log.debug('Trying to drawing pipes plot')
        y_all_pipes = station.get_all_pipes_char_vals(unit)
        l_all_pipes = 'g-'
        log.debug('x: {}, y: {}, look: {}'.format(x, y_all_pipes, l_all_pipes))
        plot.plot(
            x, y_all_pipes(x), l_all_pipes, label='char. przewodów')
    if station.pump_set_ready():
        y_set = station.pump_set.get_pumpset_vals()
        l_set = 'c-'
        plot.plot(
            x, y_set(x), l_set, label='char. zespołu pompowego')
    if station.pump_type.pump_char_ready() and station.pipes_ready():
        try:
            intersection_f = work_point(y_pump(x), y_all_pipes(x))
            plot.plot(x[intersection_f], y_pump(x)[intersection_f], 'ro',
                      label='punkt pracy')
            str_work_p = str(round(x[intersection_f][0], 2))
        except IndexError as e:
            log.error('ERROR1: {}'.format(e))
            pass
    else:
        str_work_p = ''
    str_unit = unit_bracket_dict[ui_vars.__getitem__('pump_flow_unit').get()]
    plot.set_xlabel('Przepływ Q {}'.format(str_unit))
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
    set_plot_grids(plot, unit)
    try:
        eff_from_x = station.pump_type.efficiency_from.value
        eff_from_y = interp(eff_from_x, x, y_pump(x))
        eff_to_x = station.pump_type.efficiency_to.value
        eff_to_y = interp(eff_to_x, x, y_pump(x))
        plot.plot([eff_from_x, eff_from_x], [-100, eff_from_y], 'r--')
        plot.plot([eff_to_x, eff_to_x], [-100, eff_to_y], 'r--',
                  label='maks. wydajność pompy')
        work_p_x = x[intersection_f]
        log.info('work_p_x: {}'.format(work_p_x))
        work_p_y = [interp(i, x, y_pump(x)) for i in work_p_x]
        for i in range(len(work_p_x)):
            plot.plot([work_p_x[i], work_p_x[i]],
                      [-100, work_p_y[i]], color='black',
                      linewidth=.8)
    except UnboundLocalError as e:
        log.error('Unbound ERROR2: {}'.format(e))
        pass
    if n == 1:
        half_height = (y_all_pipes(0) - y_pump(x[-1])) / 2
        y_top_lim = min(y_all_pipes(x[-1]) + 5, 1.2 * y_pump(x[0]))
    elif n > 1:
        y_top_lim = min(y_all_pipes(x[-1]) + 5, 1.2 * y_set(x[0]))
        half_height = (y_all_pipes(0) - y_set(x[-1])) / 2
    y_bot_lim = max(0, half_height)
    log.debug('x[-1] = {}'.format(x[-1]))
    plot.set_xlim(left=x[0], right=x[-1])
    plot.set_ylim(bottom=y_bot_lim, top=y_top_lim)
    plot.legend(fontsize='small')
    canvas.draw()


def draw_pipe_figure(builder, plot, canvas, station):
    log.debug('Starting draw report figure')
    plot.clear()
    canvas.draw()
    ui_vars = builder.tkvariables
    unit = ui_vars.__getitem__('inflow_unit').get()
    geom_loss_val = station.height_to_pump(
        station.ord_bottom.value + station.minimal_sewage_level.value)
    # x = station.get_x_axis(unit)
    if unit == 'liters':
        last_x = station.inflow_max.value_liters * 1.5
    elif unit == 'meters':
        last_x = station.inflow_max.value_meters * 1.5
    x = np.linspace(0, last_x, 200)
    if station.geom_loss_ready():
        y_geom_loss = station.get_geom_loss_vector()
        l_geom_loss = 'm--'
        plot.plot(
            x, y_geom_loss(x), l_geom_loss, label='geometr. wys. podn.')
    if station.d_pipe.pipe_char_ready():
        log.debug('Drawing discharge pipe plot')
        log.debug('\nDISCHARGE PIPE\n\n')
        y_d_pipe = station.d_pipe.get_pipe_char_vals(station, unit)
        l_d_pipe = 'y-'
        log.debug('x: {}, y: {}, look: {}'.format(x, y_d_pipe, l_d_pipe))
        plot.plot(x, y_d_pipe(x) + geom_loss_val, l_d_pipe,
                  label='charakterystyka przewodu wewn.')
    if station.collector.pipe_char_ready():
        log.debug('Drawing collector plot')
        log.debug('\nCOLLECTOR\n\n')
        y_coll = station.collector.get_pipe_char_vals(station, unit)
        l_coll = 'r-'
        log.debug('x: {}, y: {}, look: {}'.format(x, y_coll, l_coll))
        plot.plot(x, y_coll(x) + geom_loss_val, l_coll,
                  label='charakterystyka przewodu zewn.')
    if station.pipes_ready():
        log.debug('Trying to drawing pipes plot')
        y_all_pipes = station.get_all_pipes_char_vals(unit)
        l_all_pipes = 'g-'
        log.debug('x: {}, y: {}, look: {}'.format(x, y_all_pipes, l_all_pipes))
        plot.plot(
            x, y_d_pipe(x) + y_coll(x) + geom_loss_val, l_all_pipes,
            label='charakterystyka zespołu przewodów')
    str_unit = unit_bracket_dict[ui_vars.__getitem__('inflow_unit').get()]
    plot.set_xlabel('Przepływ Q {}'.format(str_unit))
    plot.set_ylabel('Ciśnienie [m. sł. c.]')
    set_plot_grids(plot, unit)
    plot.set_xlim(left=0, right=x[-1])
    # plot.set_ylim(bottom=geom_loss_val - 2)
    plot.legend(fontsize='small')
    canvas.draw()


def draw_pump_figure(builder, plot, canvas, station):
    log.debug('Starting draw report figure')
    plot.clear()
    canvas.draw()
    ui_vars = builder.tkvariables
    unit = ui_vars.__getitem__('pump_flow_unit').get()
    x = station.get_x_axis(unit)
    if station.pump_type.pump_char_ready():
        l_pump = 'b-'
        y_pump = station.pump_type.draw_pump_plot()
        plot.plot(x, y_pump(x), l_pump, label='charakterystyka pompy')
    str_unit = unit_bracket_dict[ui_vars.__getitem__('inflow_unit').get()]
    plot.set_xlabel('Przepływ Q {}'.format(str_unit))
    plot.set_ylabel('Ciśnienie [m. sł. c.]')
    set_plot_grids(plot, unit)
    try:
        eff_from_x = station.pump_type.efficiency_from.value
        eff_from_y = interp(eff_from_x, x, y_pump(x))
        eff_to_x = station.pump_type.efficiency_to.value
        eff_to_y = interp(eff_to_x, x, y_pump(x))
        plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
        plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                  label='maks. wydajność pompy')
    except UnboundLocalError as e:
        log.error('Unbound ERROR2: {}'.format(e))
        pass
    plot.set_xlim(left=x[0], right=x[-1])
    plot.set_ylim(bottom=0)
    plot.legend(fontsize='small')
    canvas.draw()


def draw_schema(builder, plot, canvas, station):
    pass
