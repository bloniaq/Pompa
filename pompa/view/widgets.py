import tkinter as tk


class Widget:

    def __init__(self, variable):
        self.variable = variable

    def _bind_rewrite(self):
        self.bind('<FocusOut>', self._rewrite)
        self.bind('<Return >', self._rewrite)


class Entry(tk.Entry, Widget):

    def __init__(self, variable, *args, **kwargs):
        """variable: ViewVariable"""
        Widget.__init__(self, variable)
        tk.Entry.__init__(self, *args, **kwargs)
        self.config(textvariable=variable)
        self._bind_rewrite()

    def _rewrite(self, event):
        self.variable.sent_to_model(self.variable.get())

    def update_variable(self, new_variable):
        self.variable = new_variable
        self.config(textvariable=self.variable)
        self._bind_rewrite()


class Radiobutton(tk.Radiobutton, Widget):

    def __init__(self, variable, *args, **kwargs):
        """variable: ViewVariable"""
        Widget.__init__(self, variable)
        tk.Radiobutton.__init__(self, *args, **kwargs)
        self.config(variable=variable)
