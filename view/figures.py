import logging

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

log = logging.getLogger('pompa.figs')

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


class AppFigure():

    """
    """

    def __init__(self, app, container, dim_x, dim_y):
        self.app = app
        self.builder = app.builder
        self.station = app.station
        self.fig = Figure(figsize=(dim_x, dim_y), dpi=100)
        self.plot = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=container)

    def set_plot_grids(plot, unit):
        if unit == 'meters':
            plot.xaxis.set_minor_locator(MultipleLocator(5))
        elif unit == 'liters':
            plot.xaxis.set_minor_locator(MultipleLocator(2))
        plot.yaxis.set_minor_locator(MultipleLocator(1))
        plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        plot.grid(True, 'major', linestyle='--')


class PipeFig(AppFigure):

    def __init__(self, app, container, dim_x, dim_y):

        super().__init__(app, container, dim_x, dim_y)

    def update(self):
        log.debug('Starting draw report figure')
        self.plot.clear()
        self.canvas.draw()
        ui_vars = self.builder.tkvariables
        unit = ui_vars.__getitem__('inflow_unit').get()
        geom_loss_val = self.station.height_to_pump(
            self.station.ord_bottom.value +
            self.station.minimal_sewage_level.value)
        # x = station.get_x_axis(unit)
        if unit == 'liters':
            last_x = self.station.inflow_max.value_liters * 1.5
        elif unit == 'meters':
            last_x = self.station.inflow_max.value_meters * 1.5
        x = np.linspace(0, last_x, 200)
        if self.station.geom_loss_ready():
            y_geom_loss = self.station.get_geom_loss_vector()
            l_geom_loss = 'm--'
            self.plot.plot(
                x, y_geom_loss(x), l_geom_loss, label='geometr. wys. podn.')
        if self.station.d_pipe.pipe_char_ready():
            log.debug('Drawing discharge pipe plot')
            log.debug('\nDISCHARGE PIPE\n\n')
            y_d_pipe = self.station.d_pipe.get_pipe_char_vals(
                self.station, unit)
            l_d_pipe = 'y-'
            log.debug('x: {}, y: {}, look: {}'.format(x, y_d_pipe, l_d_pipe))
            self.plot.plot(x, y_d_pipe(x) + geom_loss_val, l_d_pipe,
                           label='charakterystyka przewodu wewn.')
        if self.station.collector.pipe_char_ready():
            log.debug('Drawing collector plot')
            log.debug('\nCOLLECTOR\n\n')
            y_coll = self.station.collector.get_pipe_char_vals(
                self.station, unit)
            l_coll = 'r-'
            log.debug('x: {}, y: {}, look: {}'.format(x, y_coll, l_coll))
            self.plot.plot(x, y_coll(x) + geom_loss_val, l_coll,
                           label='charakterystyka przewodu zewn.')
        if self.station.pipes_ready():
            log.debug('Trying to drawing pipes plot')
            y_all_pipes = self.station.get_all_pipes_char_vals(unit)
            l_all_pipes = 'g-'
            log.debug('x: {}, y: {}, look: {}'.format(
                x, y_all_pipes, l_all_pipes))
            self.plot.plot(
                x, y_d_pipe(x) + y_coll(x) + geom_loss_val, l_all_pipes,
                label='charakterystyka zespołu przewodów')
        str_unit = unit_bracket_dict[ui_vars.__getitem__('inflow_unit').get()]
        self.plot.set_xlabel('Przepływ Q {}'.format(str_unit))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        self.set_plot_grids(self.plot, unit)
        self.plot.set_xlim(left=0, right=x[-1])
        # plot.set_ylim(bottom=geom_loss_val - 2)
        self.plot.legend(fontsize='small')
        self.canvas.draw()


class PumpFig(AppFigure):

    def __init__(self, app, container, dim_x, dim_y):

        super().__init__(app, container, dim_x, dim_y)

    def update(self):
        log.debug('Starting draw report figure')
        self.plot.clear()
        self.canvas.draw()
        ui_vars = self.builder.tkvariables
        unit = ui_vars.__getitem__('pump_flow_unit').get()
        x = self.station.get_x_axis(unit)
        if self.station.pump_type.pump_char_ready():
            l_pump = 'b-'
            y_pump = self.station.pump_type.draw_pump_plot()
            self.plot.plot(x, y_pump(x), l_pump, label='charakterystyka pompy')
        str_unit = unit_bracket_dict[ui_vars.__getitem__('inflow_unit').get()]
        self.plot.set_xlabel('Przepływ Q {}'.format(str_unit))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        self.set_plot_grids(self.plot, unit)
        try:
            eff_from_x = self.station.pump_type.efficiency_from.value
            eff_from_y = self.app.interp(eff_from_x, x, y_pump(x))
            eff_to_x = self.station.pump_type.efficiency_to.value
            eff_to_y = self.app.interp(eff_to_x, x, y_pump(x))
            self.plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
            self.plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                           label='maks. wydajność pompy')
        except UnboundLocalError as e:
            log.error('Unbound ERROR2: {}'.format(e))
            pass
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=0)
        self.plot.legend(fontsize='small')
        self.canvas.draw()


class ReportFig(AppFigure):

    def __init__(self, app, container, dim_x, dim_y):

        super().__init__(app, container, dim_x, dim_y)

    def update(self):
        log.debug('Starting draw report figure')
        self.plot.clear()
        self.canvas.draw()
        ui_vars = self.builder.tkvariables
        unit = ui_vars.__getitem__('pump_flow_unit').get()
        n = self.station.number_of_pumps
        x = self.station.get_x_axis(unit, n)
        if self.station.pump_type.pump_char_ready():
            l_pump = 'b-'
            y_pump = self.station.pump_type.draw_pump_plot()
            self.plot.plot(x, y_pump(x), l_pump, label='char. jednej pompy')
        if self.station.pipes_ready():
            log.debug('Trying to drawing pipes plot')
            y_all_pipes = self.station.get_all_pipes_char_vals(unit)
            l_all_pipes = 'g-'
            log.debug('x: {}, y: {}, look: {}'.format(
                x, y_all_pipes, l_all_pipes))
            self.plot.plot(
                x, y_all_pipes(x), l_all_pipes, label='char. przewodów')
        if self.station.pump_set_ready():
            y_set = self.station.pump_set.get_pumpset_vals()
            l_set = 'c-'
            self.plot.plot(
                x, y_set(x), l_set, label='char. zespołu pompowego')
        if self.station.pump_type.pump_char_ready() \
           and self.station.pipes_ready():
            try:
                intersection_f = self.app.work_point(y_pump(x), y_all_pipes(x))
                self.plot.plot(
                    x[intersection_f], y_pump(x)[intersection_f],
                    'ro', label='punkt pracy')
                str_work_p = str(round(x[intersection_f][0], 2))
            except IndexError as e:
                log.error('ERROR1: {}'.format(e))
                pass
        else:
            str_work_p = ''
        str_unit = unit_bracket_dict[ui_vars.__getitem__(
            'pump_flow_unit').get()]
        self.plot.set_xlabel('Przepływ Q {}'.format(str_unit))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        try:
            if len(x[intersection_f]) == 1:
                self.plot.set_title('Punkt pracy pompy: {} {}'.format(
                    str_work_p, str_unit))
            elif len(x[intersection_f]) > 1:
                list_points = [np.around(val, 2)
                               for val in x[intersection_f]]
                self.plot.set_title('Punkty pracy pompy: {} {}'.format(
                    list_points, str_unit))
        except UnboundLocalError:
            self.plot.set_title('Punkt pracy pompy: {} {}'.format(
                str_work_p, str_unit), fontsize='small')
            pass
        self.set_plot_grids(self.plot, unit)
        try:
            eff_from_x = self.station.pump_type.efficiency_from.value
            eff_from_y = self.app.interp(eff_from_x, x, y_pump(x))
            eff_to_x = self.station.pump_type.efficiency_to.value
            eff_to_y = self.app.interp(eff_to_x, x, y_pump(x))
            self.plot.plot([eff_from_x, eff_from_x], [-100, eff_from_y], 'r--')
            self.plot.plot([eff_to_x, eff_to_x], [-100, eff_to_y], 'r--',
                           label='maks. wydajność pompy')
            work_p_x = x[intersection_f]
            log.info('work_p_x: {}'.format(work_p_x))
            work_p_y = [self.app.interp(i, x, y_pump(x)) for i in work_p_x]
            for i in range(len(work_p_x)):
                self.plot.plot([work_p_x[i], work_p_x[i]],
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
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=y_bot_lim, top=y_top_lim)
        self.plot.legend(fontsize='small')
        self.canvas.draw()


class Schema(AppFigure):

    def __init__(self, app, container, dim_x, dim_y):

        super().__init__(app, container, dim_x, dim_y)
