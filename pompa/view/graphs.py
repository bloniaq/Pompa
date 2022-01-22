from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PipesGraph(FigureCanvasTkAgg):

    def __init__(self, master):
        fig = Figure(figsize=(5, 4), dpi=100)
        FigureCanvasTkAgg.__init__(self, fig, master)

        self.draw()

    def pack(self, *args, **kwargs):
        return self.get_tk_widget().pack(*args, **kwargs)
