import pompa.view.buttonframe as bf
import pompa.view.dataframe as df
import pompa.view.pipeframe as pipef
import pompa.view.pumpframe as pumpf
import pompa.view.variables as vv

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
        self.vars = View._create_view_variables(data)

        # initialize parameters
        self.callbacks = {}
        self.values_port = None

        # build widgets
        self.gui = Gui(self)
        self.menubar = Menu(self)
        self.title("Pompa")
        self.data_widgets = self._create_widget_dictionary()

    @staticmethod
    def _create_view_variables(data: list) -> dict:
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

        for variable in data:
            # create ViewVariable
            view_variables[variable.name] = types[variable.type](variable.name)
            # bind ViewVariable to VMVariable attribute
            variable.viewvar = view_variables[variable.name]
            view_variables[variable.name].sent_to_model = variable.set_in_model
            # set default value if exist
            if variable.default_value is not None:
                variable.viewvar.set(variable.default_value)

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

    # def add_callback(self, key, method):
    #     """Lets controller point, what method bind to widget commands"""
    #     self.callbacks[key] = method

    def add_port(self, port):
        """Lets controller point, where to send variables values

        :param port: method or function

        """
        self.values_port = port

    def bind_callbacks(self):
        self.load_button.config(command=self.callbacks["load_data"])
        self.save_button.config(command=self.callbacks["save_data"])
        self.unit_radio_meters.config(command=self.callbacks["change_units"])
        self.unit_radio_liters.config(command=self.callbacks["change_units"])
        self.safety_radio_econ.config(command=self.callbacks["set_safety"])
        self.safety_radio_opti.config(command=self.callbacks["set_safety"])
        self.safety_radio_safe.config(command=self.callbacks["set_safety"])
        self.mode_radio_check.config(command=self.callbacks["set_mode"])
        self.mode_radio_minimal.config(command=self.callbacks["set_mode"])
        self.calc_button.config(command=self.callbacks["calculate"])

    def get_var(self, name):
        return self.vars[name]

    ###
    # Controller steering section
    ###

    def draw_figure(self, figure: str):
        """Returns method for drawing desirable figure

        :param figure: str
        :return: method
        """
        methods = {
            'ins_pipe': self.gui.pipeframe.chart.draw_inside_pipe_plot,
            'geometric_height': self.gui.pipeframe.chart.draw_geometric_height
        }
        return methods[figure]

    # TODO: Not connected
    def load_datafile(self):
        filename = fd.askopenfilename(
            filetypes=[("Plik tekstowy", "*.txt")])
        # Calling Open File dialog window
        if filename:
            with open(filename, "r", -1, "utf-8") as file:
                self.data.delete(1.0, tk.END)
                self.data.insert(tk.END, file.read())

    def _remove_point(self):
        # TODO: Remove point from treeview method

        selected_items = self.points_tview.selection()
        for selected_item in selected_items:
            self.points_tview.delete(selected_item)

    ###
    # Private View methods
    ###

    def _send_value(self, widget):
        """Method provides that bound widget send its data to the controller"""
        variable = widget.variable
        var_id = variable.id
        value = variable.get()
        return self.values_port(var_id, value)

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


class Gui(tk.Frame):

    def __init__(self, view):
        parent = view
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

    def update_units(self):
        self.pumpframe.update_units()
        self.dataframe.update_units()


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


# if __name__ == "__main__":
#     view = View()
#     view.run()


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
