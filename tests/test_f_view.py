import pompa.application as app_module
import pompa.view.gui_tk as view_module
import pompa.view.variables as vv
import pompa.view.widgets as vw


class Test_Gui:

    VARIABLES = app_module.Application.VARIABLES

    def test_init(self):
        view = view_module.View(self.VARIABLES)
        assert view.vars['shape'].get() == 'round'

        """
        assert gui.ui_vars.__getitem__('mode').get() == 'minimalisation'
        diam_entry_st = gui.builder.get_object('Entry_Well_diameter').cget(
            'state')
        leng_entry_st = gui.builder.get_object('Entry_Well_length').cget(
            'state')
        wid_entry_st = gui.builder.get_object('Entry_Well_width').cget('state')
        assert str(diam_entry_st) == 'disabled'
        assert str(leng_entry_st) == 'disabled'
        assert str(wid_entry_st) == 'disabled'
        """

    def test_sending_value(self):
        view = view_module.View(self.VARIABLES)

        def port(id, value):
            return id, value

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

