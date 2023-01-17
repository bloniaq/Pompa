from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


class PipesGraph:
    # DPI rate is a monitor property
    DPI = 81
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 510

    def __init__(self, master):
        # This formula lets define figure dimensions in pixels
        fig = plt.figure(figsize=(self.PIX_X/self.DPI, self.PIX_Y/self.DPI),
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

    def set_plot_grids(self, x, unit):
        # if unit == 'm3ph':
        #     self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        # elif unit == 'lps':
        #     self.plot.xaxis.set_minor_locator(MultipleLocator(2))
        # elif unit == 'm3ps':
        #     self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        self.plot.yaxis.set_minor_locator(MultipleLocator(5))
        # self.plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        # self.plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        self.plot.grid(True, 'major', linestyle='--')
        unit_bracket_dict = {'lps': '[l/s]', 'm3ph': '[m³/h]', 'm3ps': '[m³/s]'}
        self.plot.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict['m3ps']))
        self.plot.set_ylabel('Strata ciśnienia [m. sł. c.]')

        def m3ps2lps(x):
            return x * 1000

        def lps2m3ps(x):
            return x * 0.001

        def m3ps2m3ph(x):
            return x * 3600

        def m3ph2m3ps(x):
            return x / 3600

        if unit == 'lps':
            secax = self.plot.secondary_xaxis('top', functions=(m3ps2lps, lps2m3ps))
        elif unit == 'm3ph':
            secax = self.plot.secondary_xaxis('top', functions=(m3ps2m3ph, m3ph2m3ps))
        secax.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict[unit]))
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.legend(fontsize='small')

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
        unit = self.master.view.vars['unit'].get()
        print('unit from view: ', unit)

        if self._last_data is not None:
            if unit == self._last_unit and self.new_data(data):
                return "no new data for pipe chart"
        self._last_data = data
        self._last_unit = unit

        self.clear()

        if data['x'] is None:
            return "cleared"

        methods = {
            'y_geom_h': self.draw_geometric_height,
            'y_ins_pipe': self.draw_inside_pipe_plot,
            'y_out_pipe': self.draw_outside_pipe_plot,
            'y_coop': self.draw_both_pipe_plot
        }

        for figure in data.keys():
            if figure != 'x' and data[figure]:
                print("DRAWING {}".format(figure))
                methods[figure](data['x'], data[figure], unit)

        return "pipechart updated"



    def draw_geometric_height(self, x, y, unit):
        self.plot.plot(x, y(x), 'm--', label='geometr. wys. podn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def draw_inside_pipe_plot(self, x, y, unit):
        self.plot.plot(x, y(x), 'r--', label='charakterystyka przewodu wewn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def draw_outside_pipe_plot(self, x, y, unit):
        self.plot.plot(x, y(x), 'b--', label='charakterystyka przewodu zewn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def draw_both_pipe_plot(self, x, y, unit):
        self.plot.plot(x, y(x), 'y--', label='charakterystyka przewodu zewn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def new_data(self, data):
        comp_x = data['x'] == self._last_data['x']
        comp_y_geom_h = data['y_geom_h'] == self._last_data['y_geom_h']
        comp_y_ins_pipe = data['y_ins_pipe'] == self._last_data['y_ins_pipe']
        comp_y_out_pipe = data['y_out_pipe'] == self._last_data['y_out_pipe']
        comp_y_coop = data['y_coop'] == self._last_data['y_coop']
        return all([
            comp_x.all(),
            comp_y_geom_h.all(),
            comp_y_ins_pipe.all(),
            comp_y_out_pipe.all(),
            comp_y_coop.all()
        ])

class PumpGraph:
    # DPI rate is a monitor property
    DPI = 81
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 490

    def __init__(self, master):
        # This formula lets define figure dimensions in pixels
        fig = plt.figure(figsize=(self.PIX_X/self.DPI, self.PIX_Y/self.DPI),
                         dpi=self.DPI)
        self.plot = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master)

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.canvas.get_tk_widget().pack(*args, **kwargs)

    def set_plot_grids(self, x, unit):
        if unit == 'meters':
            self.plot.xaxis.set_minor_locator(MultipleLocator(5))
        elif unit == 'liters':
            self.plot.xaxis.set_minor_locator(MultipleLocator(2))
        self.plot.yaxis.set_minor_locator(MultipleLocator(1))
        # self.plot.grid(True, 'minor', linestyle='--', linewidth=.3)
        self.plot.grid(True, 'major', linestyle='--')
        unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}
        self.plot.set_xlabel('Przepływ Q {}'.format(unit_bracket_dict[unit]))
        self.plot.set_ylabel('Ciśnienie [m. sł. c.]')
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.set_ylim(bottom=0)
        self.plot.legend(fontsize='small')

    def draw_characteristic(self, x, y, unit):
        self.plot.plot(x, y(x), 'b-', label='charakterystyka pompy')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def draw_efficiency(self, x, y, unit):
        eff_from_x = y[0]
        eff_from_y = y[1]
        eff_to_x = y[2]
        eff_to_y = y[3]
        self.plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
        self.plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                       label='maks. wydajność pompy')
        self.set_plot_grids(x, unit)
        self.canvas.draw()
