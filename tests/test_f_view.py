import pompa.application as app_module


class Test_Gui:

    def test_init(self):
        app = app_module.Application()
        gui = app.view_gui
        assert gui.ui_vars.__getitem__('shape').get() == 'rectangle'
        assert gui.ui_vars.__getitem__('mode').get() == 'minimalisation'
        diam_entry_st = gui.builder.get_object('Entry_Well_diameter').cget(
            'state')
        leng_entry_st = gui.builder.get_object('Entry_Well_length').cget(
            'state')
        wid_entry_st = gui.builder.get_object('Entry_Well_width').cget('state')
        assert str(diam_entry_st) == 'disabled'
        assert str(leng_entry_st) == 'disabled'
        assert str(wid_entry_st) == 'disabled'
