import tkinter as tk


class ViewVariable:
    """ Abstract class intended to provide additional id parameter for
    subclassed tkinter variables."""

    def __init__(self, var_id):
        self.id = var_id


class StringVar(tk.StringVar, ViewVariable):
    """Class to wrap id parameter around standard tk.StringVar """

    def __init__(self, id_, *args, **kwargs):
        ViewVariable.__init__(self, id_)
        tk.StringVar.__init__(self, *args, **kwargs)


class IntVar(tk.IntVar, ViewVariable):
    """Class to wrap id parameter around standard tk.IntVar"""

    def __init__(self, id_, *args, **kwargs):
        ViewVariable.__init__(self, id_)
        tk.IntVar.__init__(self, *args, **kwargs)

class DoubleVar(tk.DoubleVar, ViewVariable):
    """Class to wrap id parameter around standard tk.DoubleVar"""

    def __init__(self, id_, *args, **kwargs):
        ViewVariable.__init__(self, id_)
        tk.DoubleVar.__init__(self, *args, **kwargs)

class PumpCharVar():
    # placeholder for now
    def __init__(self, *args):
        pass
