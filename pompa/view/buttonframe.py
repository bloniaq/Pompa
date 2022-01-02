import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


class Buttonframe(tk.Frame):

    def __init__(self, parent, unit_var, unit_change_command):
        tk.Frame.__init__(self, parent,
                          relief='groove',
                          bd=2)
        self.parent = parent

        self.unit_var = unit_var
        self.change_unit = unit_change_command

        self.inner_frame = tk.Frame(self)
        self.inner_frame.pack(expand=True,
                              fill=tk.Y,
                              padx=20, pady=20)
        self._files_frame()
        self._units_frame()
        self._safety_frame()
        self._workmode_frame()

        self.calc_button = tk.Button(self.inner_frame,
                                     text='Oblicz',
                                     pady=8,
                                     command=self._calculate)
        self.calc_button.pack(expand=True,
                              side=tk.BOTTOM,
                              fill=tk.BOTH)

    def _change_unit(self):
        self.change_unit()

    def _files_frame(self):
        self.files_frame = tk.Frame(self.inner_frame)
        self.load_button = tk.Button(self.files_frame,
                                     text='Wczytaj Dane',
                                     command=self._open_file,
                                     padx=20, pady=5)
        self.save_button = tk.Button(self.files_frame,
                                     text='Zapisz Dane',
                                     command=self._save_file,
                                     padx=20, pady=5)
        self.load_button.pack(side=tk.LEFT)
        self.save_button.pack(side=tk.RIGHT)
        self.files_frame.pack(fill=tk.Y,
                              pady=10)

    def _units_frame(self):
        self.units_lframe = tk.ttk.Labelframe(self.inner_frame,
                                              text='Jednostki',
                                              relief='groove')
        self.units_frame = tk.Frame(self.units_lframe)
        self.meters_radio = tk.Radiobutton(self.units_frame,
                                           variable=self.unit_var,
                                           text='m³/h',
                                           value='meters',
                                           font=20,
                                           command=self._change_unit)
        self.liters_radio = tk.Radiobutton(self.units_frame,
                                           variable=self.unit_var,
                                           text='l/s',
                                           value='liters',
                                           font=20,
                                           command=self._change_unit)
        self.meters_radio.pack(side=tk.LEFT)
        self.liters_radio.pack(side=tk.RIGHT)
        self.units_frame.pack(fill=tk.X,
                              padx=40, pady=15)
        self.units_lframe.pack(fill=tk.X,
                               pady=10)

    def _safety_frame(self):
        self.safety_var = tk.StringVar()
        self.safety_var.set('optimal')

        self.safety_lframe = tk.ttk.Labelframe(self.inner_frame,
                                               text='Wariant bezpieczeństwa',
                                               relief='groove')
        self.safety_frame = tk.Frame(self.safety_lframe)
        self.econ_radio = tk.Radiobutton(self.safety_frame,
                                         variable=self.safety_var,
                                         text='Ekonomiczny',
                                         value='economic',
                                         anchor=tk.W)
        self.optim_radio = tk.Radiobutton(self.safety_frame,
                                          variable=self.safety_var,
                                          text='Optymalny',
                                          value='optimal',
                                          anchor=tk.W)
        self.safe_radio = tk.Radiobutton(self.safety_frame,
                                         variable=self.safety_var,
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
        self.safety_lframe.pack(fill=tk.X,
                                pady=10)

    def _workmode_frame(self):
        self.mode = tk.StringVar()
        self.mode.set('checking')

        self.workmode_lframe = tk.ttk.Labelframe(self.inner_frame,
                                                 text="Tryb obliczeń",
                                                 relief='groove')
        self.workmode_frame = tk.Frame(self.workmode_lframe)
        self.checking_radio = tk.Radiobutton(self.workmode_frame,
                                             variable=self.mode,
                                             text='Sprawdzenie istn. pompowni',
                                             value='checking',
                                             anchor=tk.W)
        self.minimalisation_radio = tk.Radiobutton(self.workmode_frame,
                                                   variable=self.mode,
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
        self.workmode_lframe.pack(fill=tk.X,
                                  pady=(10, 20))

    def _calculate(self):
        print('obliczenia')

    def _open_file(self):
        filename = fd.askopenfilename(
            filetypes=[("Plik tekstowy", "*.txt")])
        # wywołanie okna dialogowego open file
        if filename:
            with open(filename, "r", -1, "utf-8") as file:
                self.data.delete(1.0, tk.END)
                self.data.insert(tk.END, file.read())

    def _save_file(self):
        # TODO: Zapisz Dane do zakodowania
        pass
