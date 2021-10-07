import pompa.application as pompa

class Test_Application:

    def test_app_init(self):

        app = pompa.Application()
        assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        app = pompa.Application()
        assert isinstance(app.view_gui, pompa.gui_tk.Gui)

    def test_gui_var_to_model(self):
        app = pompa.Application()
        value = 2.1
        app.view_gui.ui_vars('well_diameter').set(value)
        # app.gui_var_to_model('well_diameter')
        assert app.station.well.diameter.value == value

    def test_model_to_gui_var(self):
        app = pompa.Application()
        value = 4.2
        app.station.well.diameter.set(value)
        assert app.view_gui.ui_vars('well_diameter').get() == value
