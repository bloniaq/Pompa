import pompa.__main__ as pompa


def test_app_init():

    app = pompa.Application()
    assert isinstance(app, pompa.Application)


def test_gui_tkinter():
    app = pompa.Application()
    assert isinstance(app.gui_tkinter, pompa.gui_tk.Gui)
