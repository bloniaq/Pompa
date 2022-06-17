import tkinter as tk

import pompa.application as app_module


class TestController:

    def test_binding_variables(self):
        with app_module.Application() as controller:
            model_pointer = controller.model.hydr_cond.ord_terrain
            model_finder = controller.model.get_var("ord_terrain")
            assert model_pointer is model_finder

            for v in controller.variables:
                if v.name == "ord_terrain":
                    vm_var = v
                    break
            assert vm_var._modelvar() is model_pointer
            model_pointer = model_pointer + model_pointer
            assert vm_var._modelvar() is model_pointer
            # assert model_pointer is model_finder

    def test_rewriting_doublevar_data_from_view_to_model(self):
        with app_module.Application() as controller:
            test_value = 11.09

            controller.view.ord_terrain_entry.delete(0, tk.END)
            controller.view.ord_terrain_entry.insert(0, test_value)

            assert controller.view.vars["ord_terrain"].get() == test_value
            assert controller.variables[6].viewvar.get() == test_value
            assert controller.variables[6].modelvar.get() == test_value

            assert controller.model.get_var("ord_terrain").value == test_value
            assert controller.model.get_var("ord_terrain").get() == test_value
            assert controller.model.hydr_cond.ord_terrain.get() == test_value
