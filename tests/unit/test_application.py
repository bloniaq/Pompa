import pompa.application as pompa
import pompa.view as view

class Test_Application:

    def test_app_init(self):

        app = pompa.Application()
        assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        app = pompa.Application()
        assert isinstance(app.view, view.gui_tk.View)
