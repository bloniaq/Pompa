import pompa.view.gui_tk_pygubu as gui_tk
import tkinter as tk
import pytest


class Test_Gui:

    def test_init(self):
        gui = gui_tk.Gui()
        assert gui is not None

    @pytest.mark.parametrize('shape, mode, diam, leng, wid', [
        ('round', 'checking', 'normal', 'disabled', 'disabled'),
        ('rectangle', 'checking', 'disabled', 'normal', 'normal'),
        ('round', 'minimalisation', 'disabled', 'disabled', 'disabled')
    ])
    def test_set_shape(self, shape, mode, diam, leng, wid):
        gui = gui_tk.Gui()
        gui.ui_set_shape(shape, mode)
        diam_entry_st = gui.builder.get_object('Entry_Well_diameter').cget(
            'state')
        leng_entry_st = gui.builder.get_object('Entry_Well_length').cget(
            'state')
        wid_entry_st = gui.builder.get_object('Entry_Well_width').cget('state')
        assert str(diam_entry_st) == diam
        assert str(leng_entry_st) == leng
        assert str(wid_entry_st) == wid
