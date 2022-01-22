from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PipesGraph(FigureCanvasTkAgg):
    # DPI rate is a monitor property
    DPI = 81
    # Figure dimensions in pixels
    PIX_X = 690
    PIX_Y = 510

    def __init__(self, master):
        # This formula lets define figure dimensions in pixels
        fig = Figure(figsize=(self.PIX_X/self.DPI, self.PIX_Y/self.DPI),
                     dpi=self.DPI)
        FigureCanvasTkAgg.__init__(self, fig, master)

        self.draw()

    def pack(self, *args, **kwargs):
        """Zastępuje pack() tak, żeby można było traktować obiekt jak widget tk
        """
        return self.get_tk_widget().pack(*args, **kwargs)
