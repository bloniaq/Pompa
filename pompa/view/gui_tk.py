import pompa.view.buttonframe as bf
import pompa.view.dataframe as df
import pompa.view.pipeframe as pipef
import pompa.view.pumpframe as pumpf
import pompa.view.variables as vv
import pompa.view.results as res

import matplotlib

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class View(tk.Tk):

    def __init__(self, data):
        """
        data: list of application variables. must provide var type and def values information
        """
        tk.Tk.__init__(self)

        # Prevents keeping unfinished processes when quiting app by 'X' button,
        # caused by matplotlib
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # initialize variables dictionary
        self.vars = self._create_view_variables(data)

        # initialize parameters
        self.callbacks = {}
        self.values_port = None

        # build widgets
        self.gui = Gui(self)
        self.menubar = Menu(self)
        self.title("Pompa")
        self.data_widgets = self._create_widget_dictionary()
        self.loadfile_procedure = None
        self.savefile_procedure = None
        self.get_results_procedure = None
        self.draw_figures_procedure = None

    def _create_view_variables(self, data: list) -> dict:
        """Create variables based on controller-provided ids"""

        view_variables = {}
        types = {
            'string': vv.StringVar,
            'int': vv.IntVar,
            'double': vv.DoubleVar,
            'res': vv.StringVar,
            'flow': vv.DoubleVar,
            'pump_char': vv.PumpCharVar
        }

        for vm_variable in data:
            # create ViewVariable
            view_variables[vm_variable.name] = types[vm_variable.type](vm_variable.name, self)
            # bind ViewVariable to VMVariable attribute
            vm_variable.viewvar = view_variables[vm_variable.name]
            view_variables[vm_variable.name].sent_to_model = vm_variable.set_in_model
            view_variables[vm_variable.name].type = vm_variable.type
            # set default value if exist
            if vm_variable.default_value is not None:
                vm_variable.viewvar.set(vm_variable.default_value)
            if vm_variable.type == 'flow' or vm_variable.type == 'pump_char':
                view_variables[vm_variable.name].get_value_for_unit = vm_variable.return_value_for_unit

        return view_variables

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def run(self):
        self.mainloop()

    def quit(self):
        """Makes sure matplotlib plots are close with closing tkinter"""
        self.destroy()
        matplotlib.pyplot.close('all')
        tk.Tk.quit(self)

    def draw_figs_callback(self, *args):
        print('oh yes oh yes')
        print('args:', args)
        self.draw_figures_procedure()

    def get_var(self, name):
        return self.vars[name]

    def get_current_unit(self):
        return self.vars['unit'].get()

    ###
    # Controller steering section
    ###

    def update_figures(self, pipechart_data, pumpchart_data):
        pipechart_result = self.gui.pipeframe.chart.draw_possible_figures(
            pipechart_data)
        pumpchart_result = self.gui.pumpframe.chart.draw_possible_figures(
            pumpchart_data
        )
        results = {
            'pipechart': pipechart_result,
            'pumpchart': pumpchart_result
        }
        return results

    def load_datafile(self):
        filename = fd.askopenfilename(
            filetypes=[("Plik tekstowy", "*.DAN")])
        # Calling Open File dialog window
        # poprzednia wersja - jednostka brana z ustawien - skad mi się to wzielo
        # przeciez powinna byc taka jednostka jak w danych czyli lps
        # self.loadfile_procedure(filename, self.vars['unit'].get())
        self.vars['unit'].set('lps')
        self.gui.update_units()
        self.loadfile_procedure(filename, self.vars['unit'].get())
        # TODO: changes in view provided by loaded file, i.e. shape
        self.gui.dataframe.update_shape()
        self.draw_figures_procedure()

    def save_datafile(self):
        filename = fd.asksaveasfilename(
            filetypes=[("Plik tekstowy", "*.DAN")])
        self.savefile_procedure(filename)

    def _remove_point(self):
        # TODO: Remove point from treeview method

        selected_items = self.points_tview.selection()
        for selected_item in selected_items:
            self.points_tview.delete(selected_item)
        self.draw_figures_procedure()

    ###
    # Private View methods
    ###

    def _set_default_values(self, values):
        """
        Lets the controller set default values

        :param values: dict(var_id: default_value)
        :return: None
        """
        for _id in values.keys():
            self.vars[_id].set(values[_id])

    def _create_widget_dictionary(self):
        dictionary = {}

        dictionary['ord_terrain'] = self.gui.dataframe.ord_ter_entry
        dictionary['ord_inlet'] = self.gui.dataframe.ord_inl_entry
        dictionary['ord_outlet'] = self.gui.dataframe.ord_out_entry
        dictionary['ord_bottom'] = self.gui.dataframe.ord_bottom_entry
        dictionary['ord_highest_point'] = self.gui.dataframe.ord_high_entry
        dictionary['ord_upper_level'] = self.gui.dataframe.ord_end_entry
        dictionary['reserve_height'] = self.gui.dataframe.alarm_h_entry
        dictionary['inflow_min'] = self.gui.dataframe.inflow_min_entry
        dictionary['inflow_max'] = self.gui.dataframe.inflow_max_entry
        dictionary['unit_m3ph'] = self.gui.buttonframe.meters_radio
        dictionary['unit_lps'] = self.gui.buttonframe.liters_radio

        self.load_button = self.gui.buttonframe.load_button
        self.save_button = self.gui.buttonframe.save_button
        self.unit_radio_meters = self.gui.buttonframe.meters_radio
        self.unit_radio_liters = self.gui.buttonframe.liters_radio
        self.safety_radio_econ = self.gui.buttonframe.econ_radio
        self.safety_radio_opti = self.gui.buttonframe.optim_radio
        self.safety_radio_safe = self.gui.buttonframe.safe_radio
        self.mode_radio_check = self.gui.buttonframe.checking_radio
        self.mode_radio_minimal = self.gui.buttonframe.minimalisation_radio
        self.calc_button = self.gui.buttonframe.calc_button
        self.ord_terrain_entry = self.gui.dataframe.ord_ter_entry

        return dictionary

    def calculate(self):
        print('calculations')
        results, station = self.get_results_procedure()
        res.ResultsWindow(self, results, station)


class Gui(tk.Frame):

    def __init__(self, view):
        parent = view
        self.view = view
        tk.Frame.__init__(self, parent)

        self.mainframe = tk.Frame(self)
        self.notebook = tk.ttk.Notebook(self.mainframe)
        self.notebook.pack(expand=True,
                           fill=tk.BOTH)
        self.dataframe = df.Dataframe(self.notebook, view)
        self.pipeframe = pipef.Pipeframe(self.notebook, view)
        self.pumpframe = pumpf.Pumpframe(self.notebook, view)
        self.notebook.add(self.dataframe, text='  Dane Projektowe  ')
        self.notebook.add(self.pipeframe, text="  Przewody  ")
        self.notebook.add(self.pumpframe, text='  Pompa  ')

        self.logoframe = Logo(self)
        self.buttonframe = bf.Buttonframe(self, view)

        self.mainframe.pack(expand=True,
                            fill=tk.BOTH,
                            side=tk.LEFT,
                            padx=(20, 10), pady=20)
        self.logoframe.pack(side=tk.TOP,
                            padx=(10, 20), pady=(20, 10),
                            ipadx=10, ipady=10)
        self.buttonframe.pack(expand=True,
                              fill=tk.BOTH,
                              padx=(10, 20), pady=(10, 20),
                              ipadx=10, ipady=10)
        self.pack()
        self.buttonframe.meters_radio.config(command=self.update_units)
        self.buttonframe.liters_radio.config(command=self.update_units)

    def update_units(self):
        self.pumpframe.update_units()
        self.dataframe.update_units()
        self.view.draw_figures_procedure()


class Logo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent,
                          relief='groove',
                          bd=2)
        self.logo_label = tk.Label(self, font=("Courier New", 10, "bold"),
                                   text="""POMPA   POMPA  POMPA  POMPA  POMPA
__________________________________

****   ****  *     * ****   ***
 *   * *    * * * * * *   * *   *
 ****  *    * *  *  * ****  *****
 *     *    * *     * *     *   *
 *      ****  *     * *     *   *
__________________________________

POMPA    Wersja 2.02/2022r   POMPA""")
        self.logo_label.pack(expand=True)


class Menu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        filemenu = tk.Menu(self, tearoff=0)
        helpmenu = tk.Menu(self, tearoff=0)

        def empty_method():
            pass

        filemenu.add_command(label="Wczytaj", command=empty_method)
        filemenu.add_command(label="Zapisz", command=empty_method)
        filemenu.add_separator()
        filemenu.add_command(label="Zakończ", command=empty_method)
        self.add_cascade(menu=filemenu, label="Plik")
        helpmenu.add_command(label="O Programie", command=empty_method)
        self.add_cascade(menu=helpmenu, label="Pomoc")
        master.config(menu=self)
