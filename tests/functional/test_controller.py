import tkinter as tk
import pytest

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
            assert vm_var.modelvar is model_pointer
            model_pointer = model_pointer + model_pointer
            assert vm_var.modelvar is model_pointer
            # assert model_pointer is model_finder

    # def test_rewriting_execution_on_focusout_ord_terrain_entry(self):
    #     with app_module.Application() as controller:
    #         test_value = 78.9
    #         controller.view.vars['ord_terrain'].set(test_value)
    #         assert controller.variables[9].modelvar.get != test_value
    #         controller.view.data_widgets['ord_terrain'].event_generate("<Return>")
    #         controller.view.data_widgets['ord_terrain'].event_generate("<FocusOut>", when='tail')
    #         assert controller.variables[9].modelvar.get() == test_value

    # def test_rewriting_doublevar_data_from_view_to_model(self):
    #     with app_module.Application() as controller:
    #         test_value = 11.09
    #
    #         controller.view.ord_terrain_entry.delete(0, tk.END)
    #         controller.view.ord_terrain_entry.insert(0, test_value)
    #
    #         assert controller.view.get_var("ord_terrain").get() == test_value
    #         assert controller.variables[9].viewvar.get() == test_value
    #         assert controller.variables[9].modelvar.get() == test_value
    #
    #         assert controller.model.get_var("ord_terrain").value == test_value
    #         assert controller.model.get_var("ord_terrain").get() == test_value
    #         assert controller.model.hydr_cond.ord_terrain.get() == test_value

# class TestControllerAsync:
#
#     @pytest.mark.asyncio
#     async def test_rewriting_execution_on_focusout_ord_terrain_entry(self):
#         controller = app_module.Application()
#         await controller.run_gui()
#         test_value = 78.9
#         controller.view.vars['ord_terrain'].set(test_value)
#         assert controller.variables[9].modelvar.get != test_value
#         controller.view.data_widgets['ord_terrain'].event_generate("<Return>")
#         controller.view.data_widgets['ord_terrain'].event_generate("<FocusOut>", when='tail')
#         assert controller.variables[9].modelvar.get() == test_value
#         controller.view.destroy()