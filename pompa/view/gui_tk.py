import pompa.view.buttonframe as bf
import pompa.view.dataframe as df
import pompa.view.pipeframe as pipef
import pompa.view.pumpframe as pumpf
import pompa.view.variables as vv

import tkinter as tk
from tkinter import ttk


class View:

    def __init__(self, variables_ids, default_values):
        self.root = tk.Tk()

        # initialize variables
        self.vars = self._create_view_variables(variables_ids)
        self._set_default_values(default_values)

        # build widgets
        self.gui = Gui(self.root)

        self.callbacks = {}

        self._create_widget_aliases()

    def run(self):
        self.root.mainloop()

    def add_callback(self, key, method):
        self.callbacks[key] = method

    def add_port(self, port):
        self.values_port = port

    def bind_callbacks(self):
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

    def _send_value(self, widget):
        variable = widget.variable
        var_id = variable.id
        value = variable.get()
        return self.values_port(var_id, value)

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

    def _create_view_variables(self, identificators):
        """Create variables based on controller-provided ids"""

        dictionary = {}

        for id in identificators['string_ids']:
            dictionary[id] = vv.StringVar(id)

        for id in identificators['int_ids']:
            dictionary[id] = vv.IntVar(id)

        for id in identificators['double_ids']:
            dictionary[id] = vv.DoubleVar(id)

        return dictionary

    def _set_default_values(self, values):
        for _id in values.keys():
            self.vars[_id].set(values[_id])


class Gui(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        unit_var = tk.StringVar()
        unit_var.set('meters')

        self.mainframe = Mainframe(self, unit_var)
        self.mainframe.pack(expand=True,
                            fill=tk.BOTH,
                            side=tk.LEFT,
                            padx=(20, 10), pady=20)
        self.logoframe = Logo(self)
        self.logoframe.pack(side=tk.TOP,
                            padx=(10, 20), pady=(20, 10),
                            ipadx=10, ipady=10)
        self.buttonframe = bf.Buttonframe(self, unit_var, self._unit_change)
        self.buttonframe.pack(expand=True,
                              fill=tk.BOTH,
                              padx=(10, 20), pady=(10, 20),
                              ipadx=10, ipady=10)
        self.pack()

    def _unit_change(self):
        self.mainframe.update_units()


class Mainframe(tk.Frame):

    def __init__(self, parent, unit_var):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.notebook = Notebook(self)
        self.notebook.pack(expand=True,
                           fill=tk.BOTH)
        self.dataframe = df.Dataframe(self.notebook, unit_var)
        self.pipeframe = pipef.Pipeframe(self.notebook)
        self.pumpframe = pumpf.Pumpframe(self.notebook, unit_var)
        self.notebook.add(self.dataframe, text='  Dane Projektowe  ')
        self.notebook.add(self.pipeframe, text="  Przewody  ")
        self.notebook.add(self.pumpframe, text='  Pompa  ')

    def update_units(self):
        self.pumpframe.update_units()
        self.dataframe.update_units()


class Notebook(tk.ttk.Notebook):

    def __init__(self, parent):
        tk.ttk.Notebook.__init__(self, parent)
        self.parent = parent


class Logo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent,
                          relief='groove',
                          bd=2)
        self.parent = parent
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
