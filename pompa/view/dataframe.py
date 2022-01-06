import tkinter as tk
from tkinter import ttk


class Dataframe(tk.Frame):

    def __init__(self, parent, unit_var):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.unit_var = unit_var
        self.shape_var = tk.StringVar()
        self.shape_var.set('round')

        self.geometry_var = tk.StringVar()
        self.geometry_var.set('linear')

        dataframe = self._dataframe()
        drawframe = self._drawframe()

        dataframe.pack(expand=True,
                       fill=tk.Y,
                       side=tk.LEFT,
                       padx=10)
        drawframe.pack(expand=True,
                       fill=tk.Y,
                       side=tk.RIGHT)

        self.pack(anchor=tk.W)

    def _dataframe(self):
        frame = tk.Frame(self)
        assump_lframe = tk.ttk.Labelframe(frame,
                                          text='Założenia')
        well_lframe = tk.ttk.Labelframe(frame,
                                        text='Studnia')
        assump_frame = self._assumpframe(assump_lframe)
        well_frame = self._wellframe(well_lframe)
        assump_frame.pack(expand=True,
                          fill=tk.BOTH,
                          padx=10, pady=10)
        well_frame.pack(expand=True,
                        fill=tk.BOTH,
                        padx=10, pady=10)

        assump_lframe.pack(expand=True,
                           fill=tk.BOTH,
                           pady=10)
        well_lframe.pack(expand=True,
                         fill=tk.BOTH,
                         pady=10)

        return frame

    def _assumpframe(self, parent):
        frame = tk.Frame(parent)

        income_label = tk.Label(frame,
                                text='Dopływ ścieków:')
        income_label.pack(anchor=tk.W)

        income_frame = tk.Frame(frame)
        income_frame.pack(expand=True,
                          fill=tk.Y)

        min_inc_label = tk.Label(income_frame,
                                 text='Minimalny:')
        max_inc_label = tk.Label(income_frame,
                                 text='Maksymalny:')
        min_inc_entry = tk.Entry(income_frame,
                                 width=5)
        max_inc_entry = tk.Entry(income_frame,
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
        min_inc_entry.grid(row=0, column=1, padx=(10, 2))
        max_inc_entry.grid(row=1, column=1, padx=(10, 2))
        self.min_inc_u_label.grid(row=0, column=2)
        self.max_inc_u_label.grid(row=1, column=2)

        # ORD FRAME

        ord_frame = tk.Frame(frame)
        ord_frame.pack(expand=True,
                       fill=tk.BOTH)

        ord_ter_label = tk.Label(ord_frame,
                                 text='Rzędna terenu')
        ord_inl_label = tk.Label(ord_frame,
                                 text='Rzędna dopływu ścieków',
                                 wraplength=120,
                                 justify=tk.LEFT)
        ord_out_label = tk.Label(ord_frame,
                                 text='Rzędna wylotu ścieków',
                                 wraplength=120,
                                 justify=tk.LEFT)
        ord_bottom_label = tk.Label(ord_frame,
                                    text='Rzędna dna pompowni',
                                    wraplength=120,
                                    justify=tk.LEFT)
        ord_high_label = tk.Label(ord_frame,
                                  text='Rzędna najwyższego punktu',
                                  wraplength=120,
                                  justify=tk.LEFT)
        ord_end_label = tk.Label(ord_frame,
                                 text='Rzędna zwierciadła w zb. górnym',
                                 wraplength=110,
                                 justify=tk.LEFT)
        alarm_h_label = tk.Label(ord_frame,
                                 text='Różnica między rz. wlotu, a rz. uruchomienia ostatniej pompy',
                                 wraplength=120,
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

        ord_ter_entry = tk.Entry(ord_frame,
                                 width=5)
        ord_inl_entry = tk.Entry(ord_frame,
                                 width=5)
        ord_out_entry = tk.Entry(ord_frame,
                                 width=5)
        ord_bottom_entry = tk.Entry(ord_frame,
                                    width=5)
        ord_high_entry = tk.Entry(ord_frame,
                                  width=5)
        ord_end_entry = tk.Entry(ord_frame,
                                 width=5)
        alarm_h_entry = tk.Entry(ord_frame,
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

        ord_ter_sym_label.grid(row=0, column=1, sticky=tk.E)
        ord_inl_sym_label.grid(row=1, column=1, sticky=tk.E)
        ord_out_sym_label.grid(row=2, column=1, sticky=tk.E)
        ord_bottom_sym_label.grid(row=3, column=1, sticky=tk.E)
        ord_high_sym_label.grid(row=4, column=1, sticky=tk.E)
        ord_end_sym_label.grid(row=5, column=1, sticky=tk.E)
        alarm_h_sym_label.grid(row=6, column=1, sticky=tk.E)

        ord_ter_entry.grid(row=0, column=2)
        ord_inl_entry.grid(row=1, column=2)
        ord_out_entry.grid(row=2, column=2)
        ord_bottom_entry.grid(row=3, column=2)
        ord_high_entry.grid(row=4, column=2)
        ord_end_entry.grid(row=5, column=2)
        alarm_h_entry.grid(row=6, column=2)

        ord_ter_u_label.grid(row=0, column=3, sticky=tk.W)
        ord_inl_u_label.grid(row=1, column=3, sticky=tk.W)
        ord_out_u_label.grid(row=2, column=3, sticky=tk.W)
        ord_bottom_u_label.grid(row=3, column=3, sticky=tk.W)
        ord_high_u_label.grid(row=4, column=3, sticky=tk.W)
        ord_end_u_label.grid(row=5, column=3, sticky=tk.W)
        alarm_h_u_label.grid(row=6, column=3, sticky=tk.W)

        return frame

    def update_units(self):
        if self.unit_var.get() == 'meters':
            self.min_inc_u_label.config(text='m³/h')
            self.max_inc_u_label.config(text='m³/h')
        elif self.unit_var.get() == 'liters':
            self.min_inc_u_label.config(text='l/s')
            self.max_inc_u_label.config(text='l/s')

    def _wellframe(self, parent):
        frame = tk.Frame(parent)

        shape_label = tk.Label(frame,
                               text='Kształt studni:')
        shape_label.pack(anchor=tk.W)

        round_radio = tk.Radiobutton(frame,
                                     text='kołowy',
                                     value='round',
                                     variable=self.shape_var,
                                     command=self._update_shape,
                                     anchor=tk.W)
        rectangle_radio = tk.Radiobutton(frame,
                                         text='prostokątny',
                                         value='rectangle',
                                         variable=self.shape_var,
                                         command=self._update_shape,
                                         anchor=tk.W)
        round_radio.pack(padx=20,
                         anchor=tk.W)
        rectangle_radio.pack(padx=20,
                             anchor=tk.W)

        geometry_label = tk.Label(frame,
                                  text='Rozmieszczenie pomp:')
        geometry_label.pack(anchor=tk.W)

        linear_radio = tk.Radiobutton(frame,
                                      text='jednorzędowe',
                                      variable=self.geometry_var,
                                      value='linear')
        optimal_radio = tk.Radiobutton(frame,
                                       text='optymalne',
                                       variable=self.geometry_var,
                                       value='optimal')
        linear_radio.pack(padx=20,
                          anchor=tk.W)
        optimal_radio.pack(padx=20,
                           anchor=tk.W)

        dimensions_frame = tk.Frame(frame)
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
        first_dim_entry = tk.Entry(dimensions_frame,
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
        first_dim_entry.grid(row=0, column=2)
        self.sec_dim_entry.grid(row=1, column=2)
        first_dim_u_label.grid(row=0, column=3)
        self.sec_dim_u_label.grid(row=1, column=3)

        self._update_shape()

        return frame

    def _update_shape(self):
        shape = self.shape_var.get()
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

    def _drawframe(self):
        frame = tk.Frame(self)

        return frame
