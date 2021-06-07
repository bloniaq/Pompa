import pompa.view.gui_tk


class Test_Gui:

    def test_init(self):
        gui = pompa.view.gui_tk.Gui()
        assert gui.ui_vars.__getitem__('shape').get() == 'rectangle'
        assert gui.ui_vars.__getitem__('mode').get() == 'minimalisation'
        assert gui.builder.get_object('Entry_Well_diameter').state == 'disabled'
        assert gui.ui_vars.get_object('Entry_Well_length').state == 'disabled'
        assert gui.ui_vars.get_object('Entry_Well_width').state == 'disabled'
