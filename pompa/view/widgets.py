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
        print(f'rewriting by {event.widget}')
        print(f"self.variable.type: {type(self.variable)}")
        print(f"is variable.get() exists: {self.variable.get is not None}")
        print(f"variable.get() {self.variable.get()}")
        print(f"is variable.sent() exists: {self.variable.sent_to_model is not None}")
        self.variable.sent_to_model(self.variable.get())


class Radiobutton(tk.Radiobutton, Widget):

    def __init__(self, variable, *args, **kwargs):
        """variable: ViewVariable"""
        Widget.__init__(self, variable)
        tk.Radiobutton.__init__(self, *args, **kwargs)
        self.config(variable=variable)
