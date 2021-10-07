import pompa.view.gui_tk
import pompa.application


class Test_Gui:

    def test_init(self):
        gui = pompa.view.gui_tk.Gui()
        assert gui.ui_vars('shape').get() == 'rectangle'
        assert gui.ui_vars('mode').get() == 'minimalisation'
        diam_entry_st = gui.builder.get_object('Entry_Well_diameter').cget(
            'state')
        leng_entry_st = gui.builder.get_object('Entry_Well_length').cget(
            'state')
        wid_entry_st = gui.builder.get_object('Entry_Well_width').cget('state')
        assert str(diam_entry_st) == 'disabled'
        assert str(leng_entry_st) == 'disabled'
        assert str(wid_entry_st) == 'disabled'


class Test_App:

    def test_passing_value_to_model(self):
        app = pompa.application.Application()
        assert isinstance(app.view_gui, pompa.view.gui_tk.Gui)

        well_diam_ui = app.view_gui.ui_vars('well_diameter')
        assert well_diam_ui.get() == 0

        well_diam_ui.set(2.5)
        assert well_diam_ui.get() == 2.5
        assert app.station.well.diameter.value == well_diam_ui.get()
