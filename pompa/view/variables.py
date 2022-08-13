import tkinter as tk


class ViewVariable:
    """ Abstract class intended to provide additional id parameter for
    subclassed tkinter variables."""

    def __init__(self, var_id, view):
        self.id = var_id
        self.view = view
        self.sent_to_model = None
        self.get_value_for_unit = None


class StringVar(tk.StringVar, ViewVariable):
    """Class to wrap id parameter around standard tk.StringVar """

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.StringVar.__init__(self, *args, **kwargs)


class IntVar(tk.IntVar, ViewVariable):
    """Class to wrap id parameter around standard tk.IntVar"""

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.IntVar.__init__(self, *args, **kwargs)


class DoubleVar(tk.DoubleVar, ViewVariable):
    """Class to wrap id parameter around standard tk.DoubleVar"""

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.DoubleVar.__init__(self, *args, **kwargs)

    def get_current_unit(self):
        return self.view.get_current_unit()

    def convert_unit(self, unit):
        self.set(self.get_value_for_unit(unit))


class PumpCharVar:
    # placeholder for now
    def __init__(self, *args):
        self.values = []

    def add_point(self, id_, unit, flow, height):
        pass
        # self.values.append({'id': id_,
        #                      flow})
