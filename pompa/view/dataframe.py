import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class Dataframe(tk.Frame):

    def __init__(self, parent, view, unit_var):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.view = view

        inner_frame = tk.Frame(self)
        inner_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self._dataframe(inner_frame)
        self._drawframe(inner_frame)

        self.dataframe.pack(expand=True,
                            fill=tk.Y,
                            side=tk.LEFT,
                            padx=10)
        self.drawframe.pack(expand=True,
                            fill=tk.Y,
                            side=tk.RIGHT)

        self.pack(anchor=tk.W)

    def _dataframe(self, parent):
        self.dataframe = tk.Frame(parent)
        assump_lframe = tk.ttk.Labelframe(self.dataframe,
                                          text='Założenia')
        well_lframe = tk.ttk.Labelframe(self.dataframe,
                                        text='Studnia')
        self._assumpframe(assump_lframe)
        self._wellframe(well_lframe)

        self.assumpframe.pack(expand=True,
                               fill=tk.BOTH,
                               padx=10, pady=10)
        self.wellframe.pack(expand=True,
                            fill=tk.BOTH,
                            padx=10, pady=10)

        assump_lframe.pack(expand=True,
                           fill=tk.BOTH,
                           pady=10)
        well_lframe.pack(expand=True,
                         fill=tk.BOTH,
                         pady=10)

    def _assumpframe(self, parent):
        self.assumpframe = tk.Frame(parent)

        income_label = tk.Label(self.assumpframe,
                                text='Dopływ ścieków:')
        income_label.pack(anchor=tk.W)

        income_frame = tk.Frame(self.assumpframe)
        income_frame.pack(expand=True,
                          fill=tk.Y)

        min_inc_label = tk.Label(income_frame,
                                 text='Minimalny:')
        max_inc_label = tk.Label(income_frame,
                                 text='Maksymalny:')
        self.min_inc_entry = tk.Entry(income_frame,
                                 width=5)
        self.max_inc_entry = tk.Entry(income_frame,
                                 width=5)
        self.min_inc_u_label = tk.Label(income_frame,
                                        width=4,
                                        anchor=tk.W)
        self.max_inc_u_label = tk.Label(income_frame,
                                        width=4,
                                        anchor=tk.W)

        self.update_units()

        min_inc_label.grid(row=0, column=0, sticky=tk.W, padx=(10, 0))
        max_inc_label.grid(row=1, column=0, sticky=tk.W, padx=(10, 0))
        self.min_inc_entry.grid(row=0, column=1, padx=(10, 2))
        self.max_inc_entry.grid(row=1, column=1, padx=(10, 2))
        self.min_inc_u_label.grid(row=0, column=2)
        self.max_inc_u_label.grid(row=1, column=2)

        # ORD FRAME

        ord_frame = tk.Frame(self.assumpframe)
        ord_frame.pack(expand=True,
                       fill=tk.BOTH)

        ord_ter_label = tk.Label(ord_frame,
                                 text='Rzędna terenu')
        ord_inl_label = tk.Label(ord_frame,
                                 text='Rzędna dopływu ścieków',
                                 # wraplength=120,
                                 justify=tk.LEFT)
        ord_out_label = tk.Label(ord_frame,
                                 text='Rzędna wylotu ścieków',
                                 # wraplength=120,
                                 justify=tk.LEFT)
        ord_bottom_label = tk.Label(ord_frame,
                                    text='Rzędna dna pompowni',
                                    # wraplength=120,
                                    justify=tk.LEFT)
        ord_high_label = tk.Label(ord_frame,
                                  text='Rzędna najwyższego punktu',
                                  # wraplength=120,
                                  justify=tk.LEFT)
        ord_end_label = tk.Label(ord_frame,
                                 text='Rzędna zwierciadła w zb. górnym',
                                 wraplength=160,
                                 justify=tk.LEFT)
        alarm_h_label = tk.Label(ord_frame,
                                 text='Wysokość obj. rezerwowej',
                                 wraplength=160,
                                 justify=tk.LEFT)
        ord_ter_sym_label = tk.Label(ord_frame,
                                     text='Rt=')
        ord_inl_sym_label = tk.Label(ord_frame,
                                     text='Rin=')
        ord_out_sym_label = tk.Label(ord_frame,
                                     text='Rout=')
        ord_bottom_sym_label = tk.Label(ord_frame,
                                        text='Rb=')
        ord_high_sym_label = tk.Label(ord_frame,
                                      text='Rh=')
        ord_end_sym_label = tk.Label(ord_frame,
                                     text='Re=')
        alarm_h_sym_label = tk.Label(ord_frame,
                                     text='Ha=')

        self.ord_ter_entry = tk.Entry(ord_frame,
                                 width=5)
        self.ord_inl_entry = tk.Entry(ord_frame,
                                 width=5)
        self.ord_out_entry = tk.Entry(ord_frame,
                                 width=5)
        self.ord_bottom_entry = tk.Entry(ord_frame,
                                    width=5)
        self.ord_high_entry = tk.Entry(ord_frame,
                                  width=5)
        self.ord_end_entry = tk.Entry(ord_frame,
                                 width=5)
        self.alarm_h_entry = tk.Entry(ord_frame,
                                 width=5)

        ord_ter_u_label = tk.Label(ord_frame, text='m n.p.m.')
        ord_inl_u_label = tk.Label(ord_frame, text='m n.p.m.')
        ord_out_u_label = tk.Label(ord_frame, text='m n.p.m.')
        ord_bottom_u_label = tk.Label(ord_frame, text='m n.p.m.')
        ord_high_u_label = tk.Label(ord_frame, text='m n.p.m.')
        ord_end_u_label = tk.Label(ord_frame, text='m n.p.m.')
        alarm_h_u_label = tk.Label(ord_frame, text='m')

        ord_ter_label.grid(row=0, column=0, sticky=tk.W)
        ord_inl_label.grid(row=1, column=0, sticky=tk.W)
        ord_out_label.grid(row=2, column=0, sticky=tk.W)
        ord_bottom_label.grid(row=3, column=0, sticky=tk.W)
        ord_high_label.grid(row=4, column=0, sticky=tk.W)
        ord_end_label.grid(row=5, column=0, sticky=tk.W)
        alarm_h_label.grid(row=6, column=0, sticky=tk.W)

        # ord_ter_sym_label.grid(row=0, column=1, sticky=tk.E)
        # ord_inl_sym_label.grid(row=1, column=1, sticky=tk.E)
        # ord_out_sym_label.grid(row=2, column=1, sticky=tk.E)
        # ord_bottom_sym_label.grid(row=3, column=1, sticky=tk.E)
        # ord_high_sym_label.grid(row=4, column=1, sticky=tk.E)
        # ord_end_sym_label.grid(row=5, column=1, sticky=tk.E)
        # alarm_h_sym_label.grid(row=6, column=1, sticky=tk.E)

        self.ord_ter_entry.grid(row=0, column=2)
        self.ord_inl_entry.grid(row=1, column=2)
        self.ord_out_entry.grid(row=2, column=2)
        self.ord_bottom_entry.grid(row=3, column=2)
        self.ord_high_entry.grid(row=4, column=2)
        self.ord_end_entry.grid(row=5, column=2)
        self.alarm_h_entry.grid(row=6, column=2)

        ord_ter_u_label.grid(row=0, column=3, sticky=tk.W)
        ord_inl_u_label.grid(row=1, column=3, sticky=tk.W)
        ord_out_u_label.grid(row=2, column=3, sticky=tk.W)
        ord_bottom_u_label.grid(row=3, column=3, sticky=tk.W)
        ord_high_u_label.grid(row=4, column=3, sticky=tk.W)
        ord_end_u_label.grid(row=5, column=3, sticky=tk.W)
        alarm_h_u_label.grid(row=6, column=3, sticky=tk.W)

    def update_units(self):
        unit_var_value = self.view.vars['unit'].get()
        if unit_var_value == 'meters':
            self.min_inc_u_label.config(text='m³/h')
            self.max_inc_u_label.config(text='m³/h')
        elif unit_var_value == 'liters':
            self.min_inc_u_label.config(text='l/s')
            self.max_inc_u_label.config(text='l/s')

    def _wellframe(self, parent):
        self.wellframe = tk.Frame(parent)

        shape_label = tk.Label(self.wellframe,
                               text='Kształt studni:')
        shape_label.pack(anchor=tk.W)

        self.round_radio = tk.Radiobutton(self.wellframe,
                                     text='kołowy',
                                     value='round',
                                     variable=self.view.vars['shape'],
                                     command=self._update_shape,
                                     anchor=tk.W)
        self.rectangle_radio = tk.Radiobutton(self.wellframe,
                                         text='prostokątny',
                                         value='rectangle',
                                         variable=self.view.vars['shape'],
                                         command=self._update_shape,
                                         anchor=tk.W)
        self.round_radio.pack(padx=20,
                         anchor=tk.W)
        self.rectangle_radio.pack(padx=20,
                             anchor=tk.W)

        geometry_label = tk.Label(self.wellframe,
                                  text='Rozmieszczenie pomp:')
        geometry_label.pack(anchor=tk.W)

        self.linear_radio = tk.Radiobutton(self.wellframe,
                                      text='jednorzędowe',
                                      variable=self.view.vars['config'],
                                      value='linear')
        self.optimal_radio = tk.Radiobutton(self.wellframe,
                                       text='optymalne',
                                       variable=self.view.vars['config'],
                                       value='optimal')
        self.linear_radio.pack(padx=20,
                          anchor=tk.W)
        self.optimal_radio.pack(padx=20,
                           anchor=tk.W)

        dimensions_frame = tk.Frame(self.wellframe)
        dimensions_frame.pack(expand=True,
                              fill=tk.Y)
        self.first_dim_label = tk.Label(dimensions_frame,
                                        width=12,
                                        anchor=tk.W)
        self.sec_dim_label = tk.Label(dimensions_frame,
                                      width=12,
                                      anchor=tk.W)
        self.first_dim_sym_label = tk.Label(dimensions_frame)
        self.sec_dim_sym_label = tk.Label(dimensions_frame)
        self.first_dim_entry = tk.Entry(dimensions_frame,
                                   width=5)
        self.sec_dim_entry = tk.Entry(dimensions_frame,
                                      width=5)
        first_dim_u_label = tk.Label(dimensions_frame,
                                     text='m')
        self.sec_dim_u_label = tk.Label(dimensions_frame)
        self.first_dim_label.grid(row=0, column=0,
                                  sticky=tk.W)
        self.sec_dim_label.grid(row=1, column=0,
                                sticky=tk.W)
        self.first_dim_sym_label.grid(row=0, column=1)
        self.sec_dim_sym_label.grid(row=1, column=1)
        self.first_dim_entry.grid(row=0, column=2)
        self.sec_dim_entry.grid(row=1, column=2)
        first_dim_u_label.grid(row=0, column=3)
        self.sec_dim_u_label.grid(row=1, column=3)

        self._update_shape()

    def _update_shape(self):
        shape = self.view.vars['shape'].get()
        if shape == 'round':
            self.first_dim_label.config(text='Średnica')
            self.first_dim_sym_label.config(text='D=')
            self.sec_dim_label.config(text='')
            self.sec_dim_sym_label.config(text='')
            self.sec_dim_entry.config(state='disabled')
            self.sec_dim_u_label.config(text='')
        elif shape == 'rectangle':
            self.first_dim_label.config(text='Długość')
            self.first_dim_sym_label.config(text='A=')
            self.sec_dim_label.config(text='Szerokość')
            self.sec_dim_sym_label.config(text='B=')
            self.sec_dim_entry.config(state='normal')
            self.sec_dim_u_label.config(text='m')

    def _drawframe(self, parent):
        self.drawframe = tk.Frame(parent)

        self.scheme = Image.open("./images/scheme.png")
        self.scheme.thumbnail((420, 610))

        self.img = ImageTk.PhotoImage(self.scheme)
        label = ttk.Label(self.drawframe, image=self.img)
        label.pack(expand=True, fill=tk.Y)
