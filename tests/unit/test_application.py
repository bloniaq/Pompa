import pompa.application as pompa

class Test_Application:

    def test_app_init(self):

        app = pompa.Application()
        assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        app = pompa.Application()
        assert isinstance(app.view_gui, pompa.gui_tk.Gui)
