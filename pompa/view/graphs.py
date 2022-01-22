from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class PipesGraph:
    # DPI rate is a monitor property
    DPI = 81
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 510

    def __init__(self, master):
        # This formula lets define figure dimensions in pixels
        fig, axs = plt.subplots(figsize=(self.PIX_X/self.DPI, self.PIX_Y/self.DPI),
                                dpi=self.DPI)
        self.plot = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master)

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.canvas.get_tk_widget().pack(*args, **kwargs)

    def draw_inside_pipe_plot(self, x, y):
        self.plot.plot(x, y(x), 'r--', label='charakterystyka przewodu wewn.')
        self.canvas.draw()
