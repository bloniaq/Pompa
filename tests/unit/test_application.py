import pompa.application as pompa

class Test_Application:

    def test_app_init(self):

        app = pompa.Application()
        assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        app = pompa.Application()
        assert isinstance(app.gui_tkinter, pompa.gui_tk.Gui)
