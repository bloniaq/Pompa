import tkinter as tk
import pytest

import pompa.application as app_module


class TestController:

    def test_binding_variables(self):
        with app_module.Application() as controller:
            model_pointer = controller.model.hydr_cond.ord_terrain
            model_finder = controller.model.get_var("ord_terrain")
            assert model_pointer is model_finder

            for v in controller.variables.values():
                if v.name == "ord_terrain":
                    vm_var = v
                    break
            assert vm_var.modelvar is model_pointer
            model_pointer = model_pointer + model_pointer
            assert vm_var.modelvar is model_pointer
