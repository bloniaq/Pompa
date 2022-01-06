import tkinter as tk


class Widget:

    def __init__(self, variable):
        self.variable = variable


class Entry(tk.Entry, Widget):

    def __init__(self, variable, *args, **kwargs):
        Widget.__init__(self, variable)
        tk.Entry.__init__(self, *args, **kwargs)
        self.config(textvariable=variable)


class Radiobutton(tk.Radiobutton, Widget):

    def __init__(self, variable, *args, **kwargs):
        Widget.__init__(self, variable)
        tk.Radiobutton.__init__(self, *args, **kwargs)
        self.config(variable=variable)
