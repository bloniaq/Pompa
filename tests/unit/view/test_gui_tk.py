import pompa.view.gui_tk as view_module
import pompa.view.variables as vv

import tkinter as tk


class Test_Gui:

    def test_structure(self):
        view = view_module.View()
        assert isinstance(view, view_module.View)
        assert isinstance(view.root, tk.Tk)
        # test whether 'run' is a method of gui_str:
        assert hasattr(view, 'run') and callable(getattr(view, 'run'))

    def test_add_values_port(self):
        view = view_module.View()

        def port():
            pass

        view.add_port(port)

        assert view.values_port == port


class Test_Variables:

    def test_id_attribute(self):
        sample = 'test_id'
        string_var = vv.StringVar(sample)
        assert string_var.id == sample

    def test_StringVar(self):
        test_value = 'test_value'
        string_var = vv.StringVar('id', value=test_value)
        assert string_var.get() == test_value

    def test_IntVar(self):
        test_value = 1312
        int_var = vv.IntVar('id', value=test_value)
        assert int_var.get() == test_value

    def test_DoubleVar(self):
        test_value = 13.12
        double_var = vv.DoubleVar('id', value=test_value)
        assert double_var.get() == test_value
