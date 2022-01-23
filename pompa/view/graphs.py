from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
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
        self.plot.set_ylabel('Strata ciśnienia [m. sł. c.]')
        self.plot.set_xlim(left=x[0], right=x[-1])
        self.plot.legend(fontsize='small')

    def draw_geometric_height(self, x, y, unit):
        self.plot.plot(x, y(x), 'm--', label='geometr. wys. podn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()

    def draw_inside_pipe_plot(self, x, y, unit):
        self.plot.plot(x, y(x), 'r--', label='charakterystyka przewodu wewn.')
        self.set_plot_grids(x, unit)
        self.canvas.draw()


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

    def draw_efficiency(selfself, x, y, unit):
        eff_from_x = y[0]
        eff_from_y = y[1]
        eff_to_x = y[2]
        eff_to_y = y[3]
        self.plot.plot([eff_from_x, eff_from_x], [0, eff_from_y], 'r--')
        self.plot.plot([eff_to_x, eff_to_x], [0, eff_to_y], 'r--',
                       label='maks. wydajność pompy')
        self.set_plot_grids(x, unit)
        self.canvas.draw()
