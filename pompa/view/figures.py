from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter

X_MULTIPLIER = {'lps': 1000, 'm3ps': 1, 'm3ph': 3600}


class DynamicGraph:
    # DPI rate is a monitor property
    DPI = 81

    def __init__(self, master, pix_x, pix_y):
        fig = plt.figure(figsize=(pix_x / self.DPI, pix_y / self.DPI),
                         dpi=self.DPI)
        self.master = master
        self._last_data = None
        self._last_unit = None
        self.plot = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master)

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.canvas.get_tk_widget().pack(*args, **kwargs)

    def clear(self):
        self.plot.clear()
        self.canvas.draw()


class PipesGraph(DynamicGraph):
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 510

    def __init__(self, master):
        super().__init__(master, self.PIX_X, self.PIX_Y)

    def draw_possible_figures(self, data):
        """

        :param data: dict
                        x: numpy.linspace or None
                        y_geom_h: np.polynomial.polynomial.Polynomial or None
                        y_ins_pipe: np.polynomial.polynomial.Polynomial or None
                        y_out_pipe: np.polynomial.polynomial.Polynomial or None
                        y_coop: np.polynomial.polynomial.Polynomial or None
        :return:
        """
        if data['x'] is None:
            self.clear()
            return "pipechart cleared"

        unit = self.master.view.vars['unit'].get()

        if self._last_data is not None:
            if unit == self._last_unit and self._same_data(data):
                return "no new data for pipechart"
        self._last_data = data
        self._last_unit = unit

        self.clear()

        methods = {
            'y_geom_h': self.draw_geometric_height,
            'y_ins_pipe': self.draw_inside_pipe_plot,
            'y_out_pipe': self.draw_outside_pipe_plot,
            'y_coop': self.draw_both_pipe_plot
        }
        x_mul = X_MULTIPLIER[unit]
        for figure in methods.keys():
            if data[figure]:
                print(data[figure])
                print("DRAWING {}".format(figure))
                methods[figure](x_mul * data['x'],
                                data[figure](data['x']))

        self.set_plot_grids(x_mul * data['x'], unit)
        self.canvas.draw()

        return "pipechart updated"

    def set_plot_grids(self, x, unit):
        if unit == 'm3ph':
            self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        elif unit == 'lps':
            self.plot.xaxis.set_minor_locator(MultipleLocator(2))
        elif unit == 'm3ps':
            self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        self.plot.yaxis.set_minor_locator(MultipleLocator(5))
        self.plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        self.plot.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        # self.plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        self.plot.grid(True, 'major', linestyle='--')
        unit_bracket_dict = {'lps': '[l/s]', 'm3ph': '[m³/h]', 'm3ps': '[m³/s]'}
        self.plot.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict[unit]))
        self.plot.set_ylabel('Strata ciśnienia [m. sł. c.]')

        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.legend(fontsize='small')

    def draw_geometric_height(self, x, y):
        self.plot.plot(x, y, 'm--', label='geometr. wys. podn.')

    def draw_inside_pipe_plot(self, x, y):
        self.plot.plot(x, y, 'r--', label='charakterystyka przewodu wewn.')

    def draw_outside_pipe_plot(self, x, y):
        self.plot.plot(x, y, 'b--', label='charakterystyka przewodu zewn.')

    def draw_both_pipe_plot(self, x, y):
        self.plot.plot(x, y, 'y--', label='charakterystyka zespołu przewodów')

    def _same_data(self, data):
        """Returns if data arrays are the same as last time"""
        if set(data.keys()) != set(self._last_data.keys()):
            return False
        for key in data.keys():
            if type(data[key]) != type(self._last_data[key]):
                return False
            expression = data[key] == self._last_data[key]
            if not isinstance(data[key], bool) and not expression.all():
                return False
        return True


class PumpGraph(DynamicGraph):
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 490

    def __init__(self, master):
        # This formula lets define figure dimensions in pixels
        super().__init__(master, self.PIX_X, self.PIX_Y)

    def draw_possible_figures(self, data):
        if isinstance(data['x'], bool):
            if not data['x']:
                self.clear()
                return "pumpchart cleared"

        unit = self.master.view.vars['unit'].get()

        if self._last_data is not None:
            if unit == self._last_unit and self._same_data(data):
                return "no new data for pumpchart"
        self._last_data = data
        self._last_unit = unit

        self.clear()

        x_mul = X_MULTIPLIER[unit]

        if data['y_p_points']:
            self.draw_points(data['y_p_points'], x_mul)
        if data['y_p_char']:
            self.draw_characteristic(data['x'], data['y_p_char'], x_mul)
        if data['y_p_eff']:
            self.draw_efficiency(data['y_p_eff'], data['y_p_char'], x_mul)
        self.set_plot_grids(x_mul * data['x'], unit)
        self.canvas.draw()

        return "pumpchart updated"

    def set_plot_grids(self, x, unit):
        # if unit == 'm3ph':
        #     self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        # elif unit == 'lps':
        #     self.plot.xaxis.set_minor_locator(MultipleLocator(2))
        # self.plot.yaxis.set_minor_locator(MultipleLocator(1))
        # self.plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        self.plot.grid(True, 'major', linestyle='--')
        unit_bracket_dict = {'lps': '[l/s]', 'm3ph': '[m³/h]'}
        self.plot.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict[unit]))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=0)
        self.plot.legend(fontsize='small')

    def draw_characteristic(self, x, y, mul):
        self.plot.plot(x * mul, y(x), 'b-', label='charakterystyka pompy')

    def draw_points(self, coords, mul):
        x_coords = [mul * c for c in coords[0]]
        self.plot.scatter(x_coords, coords[1])

    def draw_efficiency(self, values, y_pump, mul):
        eff_from_x = mul * values[0]
        eff_from_y = y_pump(eff_from_x / mul)
        eff_to_x = mul * values[1]
        eff_to_y = y_pump(eff_to_x / mul)
        self.plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
        self.plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                       label='obszar maks. wydajności pompy')

    def _same_data(self, data):
        """Returns if data arrays are the same as last time"""
        if set(data.keys()) != set(self._last_data.keys()):
            return False
        for key in data.keys():
            if type(data[key]) != type(self._last_data[key]):
                return False
            expression = data[key] == self._last_data[key]
            if type(data[key]) is bool or type(self._last_data[key]) is bool:
                if not expression:
                    return False
            if not type(expression) == bool:
                if not expression.all():
                    return False
        return True


class ResultGraph:
    # DPI rate is a monitor property
    DPI = 81
    # PIX_X = 690
    # PIX_Y = 490

    def __init__(self, parent, pix_x, pix_y, data):
        fig = plt.figure(figsize=(pix_x / self.DPI, pix_y / self.DPI),
                         dpi=self.DPI)
        self.parent = parent
        self.data = data
        self.plot = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, parent)
        self.draw(data)
        self.canvas.draw()

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.canvas.get_tk_widget().pack(*args, **kwargs)

    def clear(self):
        self.plot.clear()
        self.canvas.draw()

    def draw(self, data):
        unit = 'lps'
        x_mul = X_MULTIPLIER[unit]

        self.draw_characteristic(data['x'], data['pumpset'], x_mul)
        self.draw_efficiency(data['pump_eff'], data['pumpset'], x_mul)
        self.draw_pipeset_stop(x_mul * data['x'], data['pipeset_stop'](data['x']))
        self.draw_workpoints(data['workpoint_start'], data['workpoint_stop'], x_mul)
        self.set_plot_grids(x_mul * data['x'], unit)

    def draw_characteristic(self, x, y, mul):
        self.plot.plot(x * mul, y(x), 'b-', label='charakterystyka pompy')

    def draw_efficiency(self, values, y_pump, mul):
        eff_from_x = mul * values[0]
        eff_from_y = y_pump(eff_from_x / mul)
        eff_to_x = mul * values[1]
        eff_to_y = y_pump(eff_to_x / mul)
        self.plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
        self.plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                       label='obszar maks. wydajności pompy')

    def draw_pipeset_stop(self, x, y):
        self.plot.plot(x, y, 'g-', label='zespół przewodów (zatrzymanie pracy)')

    def draw_pipeset_start(self, x, y):
        self.plot.plot(x, y, color='gray', linestyle='--',
                       label='zespół przewodów (uruchomienie)')

    def draw_workpoints(self, wp_start, wp_stop, xmul):
        # self.plot.plot(wp_start[0] * xmul, wp_start[1], 'bo')
        self.plot.plot(wp_stop[0] * xmul, wp_stop[1], 'ro',
                       label='punkt pracy (zatrzymanie pracy)')

    def set_plot_grids(self, x, unit):
        self.plot.grid(True, 'major', linestyle='--')
        unit_bracket_dict = {'lps': '[l/s]', 'm3ph': '[m³/h]'}
        self.plot.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict[unit]))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=0)
        self.plot.legend(fontsize='small')
