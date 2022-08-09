import tkinter as tk
import pompa.view.widgets as vw
from tkinter import ttk
import pompa.view.graphs as graphs


class Pipeframe(tk.Frame):

    E_WIDTH = 5
    RES_E_WIDTH = 16

    def __init__(self, parent, view):
        tk.Frame.__init__(self, parent)
        self.view = view

        # additional Frame prevents tk.Frames ipadx/ipady bug
        inner_frame = tk.Frame(self)
        inner_frame.pack()
        self.pack()

        self.chart_frame = tk.Frame(self)

        self._int_lframe_content(inner_frame)
        self._out_lframe_content(inner_frame)
        self._chart_content()

        self.int_lframe.pack(side=tk.LEFT,
                             padx=10, pady=10)
        self.out_lframe.pack(expand=True,
                             fill=tk.Y,
                             side=tk.RIGHT,
                             padx=10, pady=10)
        self.chart.pack()
        self.chart_frame.pack(expand=True,
                              side=tk.BOTTOM,
                              fill=tk.BOTH,
                              pady=(10, 20))

    def _int_lframe_content(self, parent_f):
        PADX = 2
        PADY = 2

        self.int_lframe = tk.ttk.Labelframe(parent_f,
                                            text='Przewód wewnętrzny',
                                            relief='groove')
        int_frame = tk.Frame(self.int_lframe)
        int_frame.pack(padx=15, pady=10)

        len_label = tk.Label(int_frame,
                             text='Długość przewodu')
        dim_label = tk.Label(int_frame,
                             text='Średnica przewodu')
        rough_label = tk.Label(int_frame,
                               text='Chropowatość przewodu')
        res_label = tk.Label(int_frame,
                             text='Wartości wsp. oporów miejsc.')
        len_label.grid(row=0, column=0, sticky=tk.W)
        dim_label.grid(row=1, column=0, sticky=tk.W)
        rough_label.grid(row=2, column=0, sticky=tk.W)
        res_label.grid(row=3, column=0, sticky=tk.W)

        len_u_label = tk.Label(int_frame,
                               text='m')
        dim_u_label = tk.Label(int_frame,
                               text='mm')
        rough_u_label = tk.Label(int_frame,
                                 text='mm')
        len_u_label.grid(row=0, column=2, sticky=tk.W)
        dim_u_label.grid(row=1, column=2, sticky=tk.W)
        rough_u_label.grid(row=2, column=2, sticky=tk.W)

        self.ins_len_entry = vw.Entry(self.view.vars['ins_pipe_length'],
                                      int_frame,
                                      justify=tk.RIGHT,
                                      width=self.E_WIDTH)
        self.ins_dim_entry = vw.Entry(self.view.vars['ins_pipe_diameter'],
                                      int_frame,
                                      justify=tk.RIGHT,
                                      width=self.E_WIDTH)
        self.ins_rough_entry = vw.Entry(self.view.vars['ins_pipe_roughness'],
                                        int_frame,
                                        justify=tk.RIGHT,
                                        width=self.E_WIDTH)
        self.ins_res_entry = vw.Entry(self.view.vars['ins_pipe_resistances'],
                                      int_frame,
                                      justify=tk.RIGHT,
                                      width=self.RES_E_WIDTH)
        self.ins_len_entry.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        self.ins_dim_entry.grid(row=1, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        self.ins_rough_entry.grid(row=2, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        self.ins_res_entry.grid(row=3, column=1, padx=PADX, pady=PADY)

        hint_label = tk.Label(int_frame,
                              font=('Arial', 8, 'italic'),
                              text='Współczynniki należy oddzielać od siebie średnikiem,\n'
                                   'jako separatora dziesiętnego należy używać kropki',
                              fg='#7d807e')
        hint_label.grid(row=4, column=0, columnspan=3)

    def _out_lframe_content(self, parent):
        PADX = 2
        PADY = 2

        self.out_lframe = tk.ttk.Labelframe(parent,
                                            text='Przewód zewnętrzny',
                                            relief='groove')
        out_frame = tk.Frame(self.out_lframe)
        out_frame.pack(padx=15, pady=10)

        len_label = tk.Label(out_frame,
                             text='Długość przewodu')
        dim_label = tk.Label(out_frame,
                             text='Średnica przewodu')
        rough_label = tk.Label(out_frame,
                               text='Chropowatość przewodu')
        res_label = tk.Label(out_frame,
                             text='Wartości wsp. oporów miejsc.')
        len_label.grid(row=0, column=0, sticky=tk.W)
        dim_label.grid(row=1, column=0, sticky=tk.W)
        rough_label.grid(row=2, column=0, sticky=tk.W)
        res_label.grid(row=4, column=0, sticky=tk.W)

        len_u_label = tk.Label(out_frame,
                               text='m')
        dim_u_label = tk.Label(out_frame,
                               text='mm')
        rough_u_label = tk.Label(out_frame,
                                 text='mm')
        len_u_label.grid(row=0, column=2, sticky=tk.W)
        dim_u_label.grid(row=1, column=2, sticky=tk.W)
        rough_u_label.grid(row=2, column=2, sticky=tk.W)

        self.out_len_entry = vw.Entry(self.view.vars['out_pipe_length'],
                                      out_frame,
                                      justify=tk.RIGHT,
                                      width=self.E_WIDTH)
        self.out_dim_entry = vw.Entry(self.view.vars['out_pipe_diameter'],
                                      out_frame,
                                      justify=tk.RIGHT,
                                      width=self.E_WIDTH)
        self.out_rough_entry = vw.Entry(self.view.vars['out_pipe_roughness'],
                                        out_frame,
                                        justify=tk.RIGHT,
                                        width=self.E_WIDTH)
        self.out_res_entry = vw.Entry(self.view.vars['out_pipe_resistances'],
                                      out_frame,
                                      justify=tk.RIGHT,
                                      width=self.RES_E_WIDTH)
        self.out_len_entry.grid(row=0, column=1, padx=PADX, pady=PADY,
                                sticky=tk.E)
        self.out_dim_entry.grid(row=1, column=1, padx=PADX, pady=PADY,
                                sticky=tk.E)
        self.out_rough_entry.grid(row=2, column=1, padx=PADX, pady=PADY,
                                  sticky=tk.E)
        self.out_res_entry.grid(row=4, column=1, padx=PADX, pady=PADY)

        par_label = tk.Label(out_frame,
                             text='Liczba równoległych przewodów')
        self.out_par_entry = vw.Entry(self.view.vars['parallel_out_pipes'],
                                      out_frame,
                                      justify=tk.RIGHT,
                                      width=self.E_WIDTH)
        par_label.grid(row=3, column=0)
        self.out_par_entry.grid(row=3, column=1, padx=PADX, pady=PADY, sticky=tk.E)

    def _chart_content(self):
        self.chart = graphs.PipesGraph(self.chart_frame)

        # len_label = tk.Label(self.chart_frame,
        #                      text='Wykres')
        # len_label.grid(row=0, column=0)
