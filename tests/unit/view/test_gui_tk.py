import pompa.view.gui_tk as gui_tk
import tkinter as tk

class Test_Gui:

    def test_structure(self):
        gui_str = gui_tk.View()
        assert isinstance(gui_str, gui_tk.View)
        assert isinstance(gui_str.root, tk.Tk)
        # test whether 'run' is a method of gui_str:
        assert hasattr(gui_str, 'run') and callable(getattr(gui_str, 'run'))