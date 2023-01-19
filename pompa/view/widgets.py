import tkinter as tk


class Widget:

    def __init__(self, variable):
        self.variable = variable

    def _bind_rewrite(self):
        self.bind('<FocusOut>', self._rewrite, add='+')
        self.bind('<Return>', self._rewrite, add='+')


class Entry(tk.Entry, Widget):

    # Variable names that changing should cause check if figure can be drawn
    VARS_TRIG_FIG_DRAW = [
        "inflow_max",
        "inflow_min",
        "ord_inlet",
        "ord_outlet",
        "ord_highest_point",
        "ins_pipe_length",
        "ins_pipe_diameter",
        "ins_pipe_roughness",
        "ins_pipe_resistances",
        "out_pipe_length",
        "out_pipe_diameter",
        "out_pipe_roughness",
        "out_pipe_resistances",
        "parallel_out_pipes",
        "pump_eff_min",
        "pump_eff_max"
    ]

    def __init__(self, variable, *args, **kwargs):
        """variable: ViewVariable"""
        Widget.__init__(self, variable)
        tk.Entry.__init__(self, *args, **kwargs)
        self.config(textvariable=variable)
        self._bind_rewrite()
        self._bind_draw_fig()

    def _rewrite(self, event):
        self.variable.sent_to_model(self.variable.get())

    def update_variable(self, new_variable):
        self.variable = new_variable
        self.config(textvariable=self.variable)
        self._bind_rewrite()

    def _bind_draw_fig(self):
        for var_name in self.VARS_TRIG_FIG_DRAW:
            if hasattr(self.variable, 'id'):
                if self.variable.id == var_name:
                    print(f"binded drawing figs to {self.variable.id}")
                    self.bind('<FocusOut>', self.variable.view.draw_figs_callback, add='+')
                    self.bind('<Return>', self.variable.view.draw_figs_callback, add='+')


class Radiobutton(tk.Radiobutton, Widget):

    def __init__(self, variable, *args, **kwargs):
        """variable: ViewVariable"""
        Widget.__init__(self, variable)
        tk.Radiobutton.__init__(self, *args, **kwargs)
        self.config(variable=variable)
