import tkinter as tk  # for python 3
import pygubu


class Gui():
    
    def __init__(self):

        self.builder = pygubu.Builder()
        self.builder.add_from_file('pompa\\view\\pompa_gui.ui')
        self.mainwindow = self.builder.get_object('Toplevel_Main')
        self.filepath = self.builder.get_object('filepath')
        self.ui_vars = self.builder.tkvariables
        self.builder.connect_callbacks(self)
