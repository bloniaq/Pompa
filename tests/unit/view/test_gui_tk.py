import pompa.view.gui_tk as view_module
import pompa.view.variables as vv
import pompa.view.widgets as vw

import pompa.application as app_module

import tkinter as tk


class Test_View:

    VARIABLES = app_module.Application.VARIABLES
    DEFAULT_VALUES = app_module.Application.DEFAULT_VALUES

    def test_structure(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as view:
            assert isinstance(view, view_module.View)
            assert isinstance(view, tk.Tk)
            # test whether 'run' is a method of gui_str:
            assert hasattr(view, 'run') and callable(getattr(view, 'run'))

    def test_add_values_port(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as view:

            def port():
                pass

            view.add_port(port)
            assert view.values_port == port

    def test_default_values(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as view:
            # view = view_module.View(self.VARIABLES, self.DEFAULT_VALUES)

            assert view.vars['shape'].get() == 'round'


class Test_Variables:

    VARIABLES = app_module.Application.VARIABLES
    DEFAULT_VALUES = app_module.Application.DEFAULT_VALUES

    def test_id_attribute(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as root:
            sample = 'test_id'
            string_var = vv.StringVar(sample, master=root)
            assert string_var.id == sample

    def test_StringVar(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as root:
            test_value = 'test_value'
            string_var = vv.StringVar('id', value=test_value, master=root)
            assert string_var.get() == test_value

    def test_IntVar(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as root:
            test_value = 1312
            int_var = vv.IntVar('id', value=test_value, master=root)
            assert int_var.get() == test_value

    def test_DoubleVar(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as root:
            test_value = 13.12
            double_var = vv.DoubleVar('id', master=root, value=test_value)
            assert double_var.get() == test_value


class Test_Widgets:

    VARIABLES = app_module.Application.VARIABLES
    DEFAULT_VALUES = app_module.Application.DEFAULT_VALUES

    def test_Entry(self):
        with view_module.View(self.VARIABLES, self.DEFAULT_VALUES) as root:
            test_id = 'test_id'
            test_value = 'test_value'
            test_variable = vv.StringVar(test_id, master=root, value=test_value)
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
