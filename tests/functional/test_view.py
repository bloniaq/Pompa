import pompa.application as app_module
import pompa.view.gui_tk as view_module
import pompa.view.variables as vv
import pompa.view.widgets as vw


class TestView:

    variables_data = app_module.Application._init_variables()

    def test_init(self):
        with view_module.View(self.variables_data) as view:
            # testing variables creating
            assert 'mode' in view.vars.keys()
            # testing default values setting
            assert view.vars['shape'].get() == 'round'

    def test_sending_value(self):
        with view_module.View(self.variables_data) as view:

            def port(_id, value):
                return _id, value

            view.add_port(port)

            test_int_id = 'test_int_id'
            test_int_value = 1916
            int_var = vv.IntVar(test_int_id, view_module, value=test_int_value)
            entry = vw.Entry(int_var)
            assert view._send_value(entry) == (test_int_id, test_int_value)

            test_string_id = 'test_string_id'
            test_string_value = 'test_string_val'
            string_var = vv.StringVar(test_string_id, view_module,
                                      value=test_string_value)
            radio = vw.Radiobutton(string_var)
            assert view._send_value(radio) == (test_string_id, test_string_value)
