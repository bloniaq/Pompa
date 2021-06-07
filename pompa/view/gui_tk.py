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

        self.ui_set_shape(self.ui_vars.__getitem__('shape').get(),
                       self.ui_vars.__getitem__('mode').get())

    def ui_set_shape(self, shape, mode):
        """Set shape of station well.

        :param shape: string
            The shape of station well
        :param mode: string
            The mode of calculations
        :return: None
        """
        diameter = self.builder.get_object('Entry_Well_diameter')
        length = self.builder.get_object('Entry_Well_length')
        width = self.builder.get_object('Entry_Well_width')
        if mode == 'checking':
            if shape == 'round':
                diameter.configure(state='normal')
                length.configure(state='disabled')
                width.configure(state='disabled')
            elif shape == 'rectangle':
                diameter.configure(state='disabled')
                length.configure(state='normal')
                width.configure(state='normal')
        else:
            diameter.configure(state='disabled')
            length.configure(state='disabled')
            width.configure(state='disabled')

    def ui_set_mode(self, mode):
        """

        :param mode:
        :return:
        """

        ord_bottom_label = self.ui_vars.__getitem__('ord_bottom_label')
        if mode == 'checking':
            ord_bottom_label.set('Rzędna dna pompowni [m]')
        elif mode == 'minimalisation':
            ord_bottom_label.set('Rzędna dna pompowni (założenie) [m]')
