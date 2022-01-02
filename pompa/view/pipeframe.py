import tkinter as tk
from tkinter import ttk


class Pipeframe(tk.Frame):

    # TODO: Generowanie ramek przewodów przerobić na jedną metodę

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.E_WIDTH = 5
        self.RES_E_WIDTH = 16

        self.inner_frame = tk.Frame(self)
        self.inner_frame.pack()
        self.pack()

        self.int_lframe = tk.ttk.Labelframe(self.inner_frame,
                                            text='Przewód wewnętrzny',
                                            relief='groove')
        self.out_lframe = tk.ttk.Labelframe(self.inner_frame,
                                            text='Przewód zewnętrzny',
                                            relief='groove')
        self.chart_frame = tk.Frame(self)

        self.int_frame = tk.Frame(self.int_lframe)
        self.int_frame.pack(padx=15, pady=10)
        self._int_lframe_content(self.int_frame)

        self.out_frame = tk.Frame(self.out_lframe)
        self.out_frame.pack(padx=15, pady=10)
        self._out_lframe_content(self.out_frame)

        self._chart_content()

        self.int_lframe.pack(side=tk.LEFT,
                             padx=10, pady=10)
        self.out_lframe.pack(expand=True,
                             fill=tk.Y,
                             side=tk.RIGHT,
                             padx=10, pady=10)
        self.chart_frame.pack(expand=True,
                              side=tk.BOTTOM,
                              fill=tk.BOTH)

    def _int_lframe_content(self, parent_f):
        PADX = 2
        PADY = 2
        len_label = tk.Label(parent_f,
                             text='Długość przewodu')
        dim_label = tk.Label(parent_f,
                             text='Średnica przewodu')
        rough_label = tk.Label(parent_f,
                               text='Chropowatość przewodu')
        res_label = tk.Label(parent_f,
                             text='Wartości wsp. oporów miejsc.')
        len_label.grid(row=0, column=0, sticky=tk.W)
        dim_label.grid(row=1, column=0, sticky=tk.W)
        rough_label.grid(row=2, column=0, sticky=tk.W)
        res_label.grid(row=3, column=0, sticky=tk.W)

        len_u_label = tk.Label(parent_f,
                               text='m')
        dim_u_label = tk.Label(parent_f,
                               text='mm')
        rough_u_label = tk.Label(parent_f,
                                 text='mm')
        len_u_label.grid(row=0, column=2, sticky=tk.W)
        dim_u_label.grid(row=1, column=2, sticky=tk.W)
        rough_u_label.grid(row=2, column=2, sticky=tk.W)

        len_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.E_WIDTH)
        dim_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.E_WIDTH)
        rough_entry = tk.Entry(parent_f,
                               justify=tk.RIGHT,
                               width=self.E_WIDTH)
        res_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.RES_E_WIDTH)
        len_entry.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        dim_entry.grid(row=1, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        rough_entry.grid(row=2, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        res_entry.grid(row=3, column=1, padx=PADX, pady=PADY)

        hint_label = tk.Label(parent_f,
                              font=('Arial', 8, 'italic'),
                              text='Współczynniki należy oddzielać od siebie średnikiem,\n'
                                   'jako separatora dziesiętnego należy używać przecinka',
                              fg='#7d807e')
        hint_label.grid(row=4, column=0, columnspan=3)

    def _out_lframe_content(self, parent_f):
        PADX = 2
        PADY = 2
        len_label = tk.Label(parent_f,
                             text='Długość przewodu')
        dim_label = tk.Label(parent_f,
                             text='Średnica przewodu')
        rough_label = tk.Label(parent_f,
                               text='Chropowatość przewodu')
        res_label = tk.Label(parent_f,
                             text='Wartości wsp. oporów miejsc.')
        len_label.grid(row=0, column=0, sticky=tk.W)
        dim_label.grid(row=1, column=0, sticky=tk.W)
        rough_label.grid(row=2, column=0, sticky=tk.W)
        res_label.grid(row=4, column=0, sticky=tk.W)

        len_u_label = tk.Label(parent_f,
                               text='m')
        dim_u_label = tk.Label(parent_f,
                               text='mm')
        rough_u_label = tk.Label(parent_f,
                                 text='mm')
        len_u_label.grid(row=0, column=2, sticky=tk.W)
        dim_u_label.grid(row=1, column=2, sticky=tk.W)
        rough_u_label.grid(row=2, column=2, sticky=tk.W)

        len_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.E_WIDTH)
        dim_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.E_WIDTH)
        rough_entry = tk.Entry(parent_f,
                               justify=tk.RIGHT,
                               width=self.E_WIDTH)
        res_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.RES_E_WIDTH)
        len_entry.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        dim_entry.grid(row=1, column=1, padx=PADX, pady=PADY,sticky=tk.E)
        rough_entry.grid(row=2, column=1, padx=PADX, pady=PADY, sticky=tk.E)
        res_entry.grid(row=4, column=1, padx=PADX, pady=PADY)

        par_label = tk.Label(parent_f,
                             text='Liczba równoległych przewodów')
        par_entry = tk.Entry(parent_f,
                             justify=tk.RIGHT,
                             width=self.E_WIDTH)
        par_label.grid(row=3, column=0)
        par_entry.grid(row=3, column=1, padx=PADX, pady=PADY, sticky=tk.E)

    def _chart_content(self):
        # TODO: Wykres matplotlib

        len_label = tk.Label(self.chart_frame,
                             text='Wykres')
        len_label.grid(row=0, column=0)
