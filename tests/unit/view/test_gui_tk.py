import pytest

import pompa.view.gui_tk as view_module
import pompa.view.variables as vv
import pompa.view.widgets as vw

import pompa.application as app_module

import tkinter as tk


class TestView:

    variables_data = app_module.Application._init_variables()

    def test_structure(self):
        with view_module.View(self.variables_data) as view:
            assert isinstance(view, view_module.View)
            assert isinstance(view, tk.Tk)
            # test whether 'run' is a method of gui_str:
            assert hasattr(view, 'run') and callable(getattr(view, 'run'))

    def test_add_values_port(self):
        with view_module.View(self.variables_data) as view:

            def port():
                pass

            view.add_port(port)
            assert view.values_port == port

    def test_get_var_method(self):
        with view_module.View(self.variables_data) as view:

            assert view.get_var('shape').get() == 'round'

    def test_rewrite_method(self):
        with view_module.View(self.variables_data) as view:
            var1 = tk.StringVar(view).set("test 1")
            entry1 = tk.Entry(view, textvariable=var1)
            var2 = tk.StringVar(view).set("test 2")
            entry2 = tk.Entry(view, textvariable=var2)

            view.data_widgets = {entry1, entry2}


class TestVariables:

    variables_data = app_module.Application._init_variables()

    def test_id_attribute(self):
        with view_module.View(self.variables_data) as root:
            sample = 'test_id'
            string_var = vv.StringVar(sample, view_module, master=root)
            assert string_var.id == sample

    def test_stringvar(self):
        with view_module.View(self.variables_data) as root:
            test_value = 'test_value'
            string_var = vv.StringVar('id', view_module, value=test_value, master=root)
            assert string_var.get() == test_value

    def test_intvar(self):
        with view_module.View(self.variables_data) as root:
            test_value = 1312
            int_var = vv.IntVar('id', view_module, value=test_value, master=root)
            assert int_var.get() == test_value

    def test_doublevar(self):
        with view_module.View(self.variables_data) as root:
            test_value = 13.12
            double_var = vv.DoubleVar('id', view_module, master=root, value=test_value)
            assert double_var.get() == test_value


class TestWidgets:

    variables_data = app_module.Application._init_variables()

    def test_entry(self):
        with view_module.View(self.variables_data) as root:
            test_id = 'test_id'
            test_value = 'test_value'
            test_variable = vv.StringVar(test_id, view_module, master=root,
                                         value=test_value,)
            entry = vw.Entry(test_variable)
            assert entry.variable == test_variable
            assert entry.variable.id == test_id
            assert entry.variable.get() == test_value
            assert entry.get() == test_value

            entry.delete(0, tk.END)
            assert entry.get() == ''

            other_value = 'other_value'
            entry.insert(0, other_value)
            assert entry.get() == other_value
