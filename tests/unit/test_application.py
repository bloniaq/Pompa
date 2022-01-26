import pompa.application as pompa
import pompa.view as view

class Test_Application:

    def test_app_init(self):
        with pompa.Application() as app:
            assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        with pompa.Application() as app:
            assert isinstance(app.view, view.gui_tk.View)
