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

        self.draw()

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.canvas.get_tk_widget().pack(*args, **kwargs)

    def pass_data(self, data):

        # OBRÓBKA DANYCH

        self.draw()

    def draw(self):
        pass