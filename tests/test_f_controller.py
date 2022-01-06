import tkinter as tk

import pompa.application as app_module


class Test_Controller:

    def test_rewriting_doublevar_data_from_view_to_model(self):
        controller = app_module.Application()

        test_value = 11.09

        controller.view.ord_terrain_entry.delete(0, tk.END)
        controller.view.ord_terrain_entry.insert(0, test_value)

        assert controller.model.ord_terrain.get() == test_value