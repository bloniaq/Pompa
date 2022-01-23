import tkinter as tk
from tkinter import ttk


class Buttonframe(tk.Frame):

    def __init__(self, parent, view):
        tk.Frame.__init__(self, parent,
                          relief='groove',
                          bd=2)
        self.view = view

        # additional Frame prevents tk.Frames ipadx/ipady bug
        inner_frame = tk.Frame(self)
        inner_frame.pack(expand=True,
                         fill=tk.Y,
                         padx=20, pady=20)

        self._files_frame(inner_frame)
        self._units_frame(inner_frame)
        self._safety_frame(inner_frame)
        self._workmode_frame(inner_frame)
        self.calc_button = tk.Button(inner_frame,
                                     text='Oblicz',
                                     pady=8)

        self.files_frame.pack(fill=tk.Y,
                              pady=5)
        self.units_lframe.pack(fill=tk.X,
                               pady=5)
        self.safety_lframe.pack(fill=tk.X,
                                pady=5)
        self.workmode_lframe.pack(fill=tk.X,
                                  pady=(5, 20))
        self.calc_button.pack(
            expand=True,
            fill=tk.BOTH,
            side=tk.BOTTOM
                              )

    def _files_frame(self, parent):
        self.files_frame = tk.Frame(parent)
        self.load_button = tk.Button(self.files_frame,
                                     text='Wczytaj Dane',
                                     padx=20, pady=5)
        self.save_button = tk.Button(self.files_frame,
                                     text='Zapisz Dane',
                                     padx=20, pady=5)
        self.load_button.pack(side=tk.LEFT)
        self.save_button.pack(side=tk.RIGHT)

    def _units_frame(self, parent):
        self.units_lframe = tk.ttk.Labelframe(parent,
                                              text='Jednostki',
                                              relief='groove')
        # additional Frame prevents tk.Frames ipadx/ipady bug
        self.units_frame = tk.Frame(self.units_lframe)
        self.meters_radio = tk.Radiobutton(self.units_frame,
                                           variable=self.view.vars['unit'],
                                           text='m³/h',
                                           value='meters',
                                           font=15)
        self.liters_radio = tk.Radiobutton(self.units_frame,
                                           variable=self.view.vars['unit'],
                                           text='l/s',
                                           value='liters',
                                           font=15)
        self.meters_radio.pack(side=tk.LEFT)
        self.liters_radio.pack(side=tk.RIGHT)
        self.units_frame.pack(fill=tk.X,
                              padx=40, pady=10)

    def _safety_frame(self, parent):
        self.safety_lframe = tk.ttk.Labelframe(parent,
                                               text='Wariant bezpieczeństwa',
                                               relief='groove')
        # additional Frame prevents tk.Frames ipadx/ipady bug
        self.safety_frame = tk.Frame(self.safety_lframe)
        self.econ_radio = tk.Radiobutton(self.safety_frame,
                                         variable=self.view.vars['safety'],
                                         text='Ekonomiczny',
                                         value='economic',
                                         anchor=tk.W)
        self.optim_radio = tk.Radiobutton(self.safety_frame,
                                          variable=self.view.vars['safety'],
                                          text='Optymalny',
                                          value='optimal',
                                          anchor=tk.W)
        self.safe_radio = tk.Radiobutton(self.safety_frame,
                                         variable=self.view.vars['safety'],
                                         text='Bezpieczny',
                                         value='safe',
                                         anchor=tk.W)
        self.econ_radio.pack(expand=True,
                             fill=tk.X)
        self.optim_radio.pack(expand=True,
                              fill=tk.X)
        self.safe_radio.pack(expand=True,
                             fill=tk.X)
        self.safety_frame.pack(side=tk.LEFT,
                               fill=tk.X,
                               padx=20, pady=(15, 5))

    def _workmode_frame(self, parent):
        self.workmode_lframe = tk.ttk.Labelframe(parent,
                                                 text="Tryb obliczeń",
                                                 relief='groove')
        # additional Frame prevents tk.Frames ipadx/ipady bug
        self.workmode_frame = tk.Frame(self.workmode_lframe)
        self.checking_radio = tk.Radiobutton(self.workmode_frame,
                                             variable=self.view.vars['mode'],
                                             text='Sprawdzenie istn. pompowni',
                                             value='checking',
                                             anchor=tk.W)
        self.minimalisation_radio = tk.Radiobutton(self.workmode_frame,
                                                   variable=self.view.vars['mode'],
                                                   text='Minimalizacja nakładów inwest.',
                                                   value='minimalisation',
                                                   anchor=tk.W)
        self.checking_radio.pack(expand=True,
                                 fill=tk.X)
        self.minimalisation_radio.pack(expand=True,
                                       fill=tk.X)
        self.workmode_frame.pack(side=tk.LEFT,
                                 fill=tk.X,
                                 padx=20, pady=15)
