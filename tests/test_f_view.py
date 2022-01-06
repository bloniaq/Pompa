import pompa.application as app_module
import pompa.view.gui_tk as view_module
import pompa.view.variables as vv
import pompa.view.widgets as vw


class Test_View:

    VARIABLES = app_module.Application.VARIABLES
    DEFAULT_VALUES = app_module.Application.DEFAULT_VALUES

    def test_init(self):
        view = view_module.View(self.VARIABLES, self.DEFAULT_VALUES)
        # testing variables creating
        assert 'mode' in view.vars.keys()
        # testing default values setting
        assert view.vars['shape'].get() == 'round'

    def test_sending_value(self):
        view = view_module.View(self.VARIABLES, self.DEFAULT_VALUES)

        def port(_id, value):
            return _id, value

        view.add_port(port)

        test_int_id = 'test_int_id'
        test_int_value = 1916
        int_var = vv.IntVar(test_int_id, value=test_int_value)
        entry = vw.Entry(int_var)
        assert view._send_value(entry) == (test_int_id, test_int_value)

        test_string_id = 'test_string_id'
        test_string_value = 'test_string_val'
        string_var = vv.StringVar(test_string_id, value=test_string_value)
        radio = vw.Radiobutton(string_var)
        assert view._send_value(radio) == (test_string_id, test_string_value)
