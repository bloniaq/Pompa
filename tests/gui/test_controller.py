import tkinter as tk

import pompa.application as app_module


class Test_Controller:

    def test_rewriting_doublevar_data_from_view_to_model(self):
        with app_module.Application() as controller:
            test_value = 11.09

            print('Initial viewvar value:')
            print(controller.get_var('ord_terrain').viewvar.get())
            print('Initial modelvar value:')
            print(controller.get_var('ord_terrain').modelvar.get())

            controller.view.gui.dataframe.ord_ter_entry.delete(0, tk.END)
            controller.view.gui.dataframe.ord_ter_entry.insert(0, test_value)

            print('Final viewvar value:')
            print(controller.get_var('ord_terrain').viewvar.get())
            print('Final modelvar value:')
            print(controller.get_var('ord_terrain').modelvar.get())

            print('Modelvar: ', controller.get_var('ord_terrain').modelvar)
            print('Modelvar.value: ', controller.get_var('ord_terrain').modelvar.value)
            print('Modelvar.get(): ', controller.get_var('ord_terrain').modelvar.get())
            print('Modelvar.name: ', controller.get_var('ord_terrain').modelvar.name)
            print('Modelvar.instances: ', controller.get_var('ord_terrain').modelvar.instances)

            print('hydr_cond.ord_terrain: ', controller.model.hydr_cond.ord_terrain)
            print('hydr_cond.ord_terrain.value: ', controller.model.hydr_cond.ord_terrain.value)
            print('hydr_cond.ord_terrain.get(): ', controller.model.hydr_cond.ord_terrain.get())
            print('hydr_cond.ord_terrain.name: ', controller.model.hydr_cond.ord_terrain.name)
            print('hydr_cond.ord_terrain.instances: ', controller.model.hydr_cond.ord_terrain.instances)

            assert float(controller.view.vars['ord_terrain'].get()) == test_value
            assert controller.model.hydr_cond.ord_terrain.get() == test_value
