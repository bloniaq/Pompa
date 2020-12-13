import pompa.view.gui_tk


def test_init():
    gui = pompa.view.gui_tk.Gui()
    assert gui is not None
