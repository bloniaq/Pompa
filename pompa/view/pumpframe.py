import tkinter as tk
from tkinter import ttk

import pompa.view.graphs as graphs


class Pumpframe(tk.Frame):

    def __init__(self, parent, view):
        tk.Frame.__init__(self, parent)
        self.view = view
        self.add_point_window = None

        inner_frame = tk.Frame(self)
        inner_frame.pack()
        self._prop_lframe(inner_frame)
        self._points_lframe(inner_frame)
        self._chart_frame()

        self.prop_lframe.pack(expand=True,
                              fill=tk.BOTH,
                              side=tk.LEFT,
                              padx=10, pady=10)
        self.points_lframe.pack(expand=True,
                                fill=tk.BOTH,
                                side=tk.RIGHT,
                                padx=10, pady=10)
        self.chart.pack()
        self.chart_frame.pack(expand=True,
                              side=tk.BOTTOM,
                              fill=tk.BOTH,
                              pady=(10, 20))
        self.pack()

    def update_units(self):
        """
        Updates content of unit labels near entries
        :return: None
        """
        unit_var_value = self.view.vars['unit'].get()
        if unit_var_value == 'meters':
            self.minran_u_label.config(text='m³/h')
            self.maxran_u_label.config(text='m³/h')
        elif unit_var_value == 'liters':
            self.minran_u_label.config(text='l/s')
            self.maxran_u_label.config(text='l/s')

    def _prop_lframe(self, parent):
        self.prop_lframe = tk.ttk.Labelframe(parent,
                                             text='Właściwości pompy')

        # additional Frame prevents tk.Frames ipadx/ipady bug
        inner_frame = tk.Frame(self.prop_lframe)
        inner_frame.pack(expand=True,
                         fill=tk.BOTH,
                         padx=30, pady=10)
        dim_label = tk.Label(inner_frame,
                             text='Średnica instalacyjna pompy')
        cycle_label = tk.Label(inner_frame,
                               text='Min. czas cyklu pompy')
        height_label = tk.Label(inner_frame,
                                text='Min. wysokość ścieków')
        range_label = tk.Label(inner_frame,
                               text='Zakres maksymalnej wydajności pompy:')
        minran_label = tk.Label(inner_frame,
                                text='Od')
        maxran_label = tk.Label(inner_frame,
                                text='Do')
        dim_u_label = tk.Label(inner_frame,
                               text='m')
        cycle_u_label = tk.Label(inner_frame,
                                 text='min')
        height_u_label = tk.Label(inner_frame,
                                  text='m')
        self.minran_u_label = tk.Label(inner_frame,
                                       width=4,
                                       anchor=tk.W)
        self.maxran_u_label = tk.Label(inner_frame,
                                       width=4,
                                       anchor=tk.W)
        dim_label.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=2)
        cycle_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=2)
        height_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=2)
        range_label.grid(row=3, column=0, columnspan=6, pady=(8, 2))
        minran_label.grid(row=4, column=0, sticky=tk.W)
        maxran_label.grid(row=4, column=3, sticky=tk.E)
        dim_u_label.grid(row=0, column=5, sticky=tk.W)
        cycle_u_label.grid(row=1, column=5, sticky=tk.W)
        height_u_label.grid(row=2, column=5, sticky=tk.W)

        self.update_units()
        self.minran_u_label.grid(row=4, column=2, padx=(0, 45))
        self.maxran_u_label.grid(row=4, column=5)

        ENTRY_WID = 7
        self.dim_entry = tk.Entry(inner_frame,
                                  justify=tk.RIGHT,
                                  width=ENTRY_WID)
        self.cycle_entry = tk.Entry(inner_frame,
                                    justify=tk.RIGHT,
                                    width=ENTRY_WID)
        self.height_entry = tk.Entry(inner_frame,
                                     justify=tk.RIGHT,
                                     width=ENTRY_WID)
        self.minran_entry = tk.Entry(inner_frame,
                                     justify=tk.RIGHT,
                                     width=ENTRY_WID)
        self.maxran_entry = tk.Entry(inner_frame,
                                     justify=tk.RIGHT,
                                     width=ENTRY_WID)

        self.dim_entry.grid(row=0, column=4, padx=2, pady=2)
        self.cycle_entry.grid(row=1, column=4, padx=2, pady=2)
        self.height_entry.grid(row=2, column=4, padx=2, pady=2)
        self.minran_entry.grid(row=4, column=1, padx=2, pady=2)
        self.maxran_entry.grid(row=4, column=4, padx=2, pady=2)

    def _points_lframe(self, parent):
        self.points_lframe = tk.ttk.Labelframe(parent,
                                               text='Charakterystyka pompy')
        # additional Frame prevents tk.Frames ipadx/ipady bug
        inner_frame = tk.Frame(self.points_lframe)
        inner_frame.pack(padx=10, pady=10)
        button_frame = tk.Frame(inner_frame)
        button_frame.pack(expand=True,
                          fill=tk.BOTH,
                          side=tk.LEFT)

        add_button = tk.Button(button_frame,
                               text='+',
                               font=('Arial', 20, 'bold'),
                               fg='green',
                               command=self._add_point_window)
        rem_button = tk.Button(button_frame,
                               text='-',
                               font=('Arial', 20, 'bold'),
                               fg='red')
        add_button.pack(expand=True,
                        side=tk.TOP,
                        fill=tk.BOTH)
        rem_button.pack(expand=True,
                        fill=tk.BOTH)

        self.points_tview = tk.ttk.Treeview(inner_frame, height=6)
        self.points_tview['columns'] = ('id', 'vflow', 'height')
        self.points_tview.column('#0', width=0, stretch=tk.NO)
        self.points_tview.column('id', anchor=tk.CENTER, width=40)
        self.points_tview.column('vflow', anchor=tk.CENTER, width=110)
        self.points_tview.column('height', anchor=tk.CENTER, width=110)
        self.points_tview.heading('#0', text='', anchor=tk.CENTER)
        self.points_tview.heading('id', text='Nr', anchor=tk.CENTER)
        self.points_tview.heading('vflow', text='Przepływ [m³/h]', anchor=tk.CENTER)
        self.points_tview.heading('height', text='Wys. podn. [m]', anchor=tk.CENTER)
        self.points_tview.pack(expand=True,
                               side=tk.LEFT,
                               fill=tk.Y)
        scrollbar = tk.ttk.Scrollbar(inner_frame, orient=tk.VERTICAL,
                                     command=self.points_tview.yview)
        self.points_tview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.LEFT,
                       fill=tk.Y)

    def _chart_frame(self):
        self.chart_frame = tk.Frame(self)
        self.chart = graphs.PumpGraph(self.chart_frame)

    def _add_point_window(self):
        if self.add_point_window is not None:
            self.add_point_window.destroy()
        self.add_point_window = AddPointWindow(self.view,
                                               self.points_tview)
        # TODO: Add point method
        pass


class AddPointWindow(tk.Toplevel):

    def __init__(self, view, treeview):
        tk.Toplevel.__init__(self, view)
        self.view = view
        self.title('Dodaj Punkt')
        self.unit_var = self.view.vars['unit']

        self.tv = treeview
        self.vflow_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()

        frame = tk.Frame(self,
                         relief='groove')
        frame.pack(padx=15, pady=15)

        data_frame = self._data_frame(frame)
        button_frame = self._button_frame(frame)

        data_frame.pack()
        button_frame.pack(expand=True,
                          fill=tk.X,
                          pady=(15, 5))

    def _data_frame(self, frame):
        data_frame = tk.Frame(frame)

        vflow_label = tk.Label(data_frame,
                               text='Przepływ Q')
        height_label = tk.Label(data_frame,
                                text='Wysokość podnoszenia H')
        vflow_label.grid(row=0, column=0, sticky=tk.E)
        height_label.grid(row=1, column=0, sticky=tk.E)

        vflow_entry = tk.Entry(data_frame,
                               justify=tk.RIGHT,
                               width=7,
                               textvariable=self.vflow_var)
        height_entry = tk.Entry(data_frame,
                                justify=tk.RIGHT,
                                width=7,
                                textvariable=self.height_var)
        vflow_entry.grid(row=0, column=1, padx=(25, 2), pady=6, sticky=tk.E)
        height_entry.grid(row=1, column=1, padx=(25, 2), pady=6, sticky=tk.E)

        self.vflow_u_label = tk.Label(data_frame,
                                      anchor=tk.W,
                                      width=4)
        self._unit_update()
        height_u_label = tk.Label(data_frame,
                                  anchor=tk.W,
                                  text='m',
                                  width=4)
        self.vflow_u_label.grid(row=0, column=2)
        height_u_label.grid(row=1, column=2)

        vflow_entry.bind('<KeyRelease-comma>', self._replace_comma)
        height_entry.bind('<KeyRelease-comma>', self._replace_comma)

        return data_frame

    def _button_frame(self, frame):
        button_frame = tk.Frame(frame)
        add_button = tk.Button(button_frame,
                               text='Dodaj Punkt',
                               padx=10, pady=5,
                               command=self._add_point)
        cancel_button = tk.Button(button_frame,
                                  text='Anuluj',
                                  padx=10, pady=5,
                                  command=self.destroy)
        add_button.pack(expand=True,
                        fill=tk.X,
                        side=tk.LEFT,
                        padx=10)
        cancel_button.pack(expand=True,
                           fill=tk.X,
                           side=tk.LEFT,
                           padx=10)
        return button_frame

    def _add_point(self):

        self.tv.insert('', tk.END, values=('x',
                                           self.vflow_var.get(),
                                           self.height_var.get()))
        self.destroy()

    def _replace_comma(self, event):
        content = event.widget.get()
        content = content.replace(',', '.')
        event.widget.delete(0, tk.END)
        event.widget.insert(0, content)

    def _unit_update(self):
        unit_var_value = self.view.vars['unit'].get()
        if unit_var_value == 'meters':
            self.vflow_u_label.config(text='m³/h')
        elif unit_var_value == 'liters':
            self.vflow_u_label.config(text='l/s')
