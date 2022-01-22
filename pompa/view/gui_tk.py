import pompa.view.buttonframe as bf
import pompa.view.dataframe as df
import pompa.view.pipeframe as pipef
import pompa.view.pumpframe as pumpf
import pompa.view.variables as vv

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class View(tk.Tk):

    def __init__(self, variables_ids, default_values):
        tk.Tk.__init__(self)

        # Prevents keeping unfinished processes when quiting app by 'X' button,
        # caused by matplotlib
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # initialize variables
        self.vars = self._create_view_variables(variables_ids)
        self._set_default_values(default_values)

        # initialize parameters
        self.callbacks = {}
        self.values_port = None

        # build widgets
        self.gui = Gui(self)
        self._create_widget_aliases()

    def run(self):
        self.mainloop()

    def quit(self):
        """Makes sure matplotlib plots are close with closing tkinter"""
        tk.Tk.quit(self)
        self.destroy()

    def add_callback(self, key, method):
        """Lets controller point, what method bind to widget commands"""
        self.callbacks[key] = method

    def add_port(self, port):
        """Lets controller point, where to send variables values"""
        self.values_port = port

    def bind_callbacks(self):
        # TODO: rewrite dict keys as verbs, since callbacks are methods, not
        #       parameters
        self.load_button.config(command=self.callbacks['load_data'])
        self.save_button.config(command=self.callbacks['save_data'])
        self.unit_radio_meters.config(command=self.callbacks['units'])
        self.unit_radio_liters.config(command=self.callbacks['units'])
        self.safety_radio_econ.config(command=self.callbacks['safety'])
        self.safety_radio_opti.config(command=self.callbacks['safety'])
        self.safety_radio_safe.config(command=self.callbacks['safety'])
        self.mode_radio_check.config(command=self.callbacks['mode'])
        self.mode_radio_minimal.config(command=self.callbacks['mode'])
        self.calc_button.config(command=self.callbacks['calculate'])

    ###
    # Controller steering section
    ###

    # TODO: Not connected
    def load_datafile(self):
        filename = fd.askopenfilename(
            filetypes=[("Plik tekstowy", "*.txt")])
        # wywołanie okna dialogowego open file
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
        """Method provides that binded widget send its data to the controller"""
        variable = widget.variable
        var_id = variable.id
        value = variable.get()
        return self.values_port(var_id, value)

    def _create_view_variables(self, identificators):
        """Create variables based on controller-provided ids"""

        dictionary = {}

        for _id in identificators['string_ids']:
            dictionary[_id] = vv.StringVar(_id)

        for _id in identificators['int_ids']:
            dictionary[_id] = vv.IntVar(_id)

        for _id in identificators['double_ids']:
            dictionary[_id] = vv.DoubleVar(_id)

        return dictionary

    def _set_default_values(self, values):
        """
        Lets the controller set default values

        :param values: dict(var_id: default_value)
        :return: None
        """
        for _id in values.keys():
            self.vars[_id].set(values[_id])

    def _create_widget_aliases(self):
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
        self.ord_terrain_entry = self.gui.dataframe


class Gui(tk.Frame):

    def __init__(self, view):
        parent = view
        tk.Frame.__init__(self, parent)

        # TODO: delete this after refactor
        unit_var = tk.StringVar()
        unit_var.set('meters')

        self.mainframe = tk.Frame(self)
        self.notebook = tk.ttk.Notebook(self.mainframe)
        self.notebook.pack(expand=True,
                           fill=tk.BOTH)
        self.dataframe = df.Dataframe(self.notebook, view, unit_var)
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
