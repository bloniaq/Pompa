import sys
import os

try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import pygubu


class Myapp:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"proba.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('Frame_1', master)

        builder.connect_callbacks(self)

        callbacks = {
            'przepisz': self.przepisz,
            'aktywacja': self.aktywacja,
            'radiobs': self.radiobs,
            'caller': self.caller
            #'walidacja, \'%W\'': self.walidacja
            }

        builder.connect_callbacks(callbacks)

    def walidacja(event, name):
        obj = event.builder.get_variable('labeltext')
        print(obj)
        print(name)
        return True

    def przepisz(self, *args):
        entry = self.builder.get_object('Entry_1')
        value = entry.get()
        print('Entry_1:', value)

        labeltext = self.builder.get_variable('labeltext')
        labeltext.set(value)

    def aktywacja(self):
        label = self.builder.get_object('Label_1')
        current_state = str(label.cget('state'))
        if current_state == 'normal' or current_state == 'active':
            new_state = 'disabled'
            print('disabling')
        else:
            new_state = 'normal'
            print('normalizing')
        label.configure(state=new_state)
        messagebox.showinfo('Aktywacja', 'Button 2 was clicked !!')

    def bitmapa(self):
        messagebox.showinfo('wykrzyknik', 'wykrzyknik')

    def radiobs(self):
        radio1 = self.builder.get_object('Radiobutton_1')
        radio2 = self.builder.get_object('Radiobutton_2')
        radio4 = self.builder.get_object('Radiobutton_4')
        radiovar = self.builder.tkvariables.__getitem__('radio').get()
        currentradio = self.builder.get_object('Radiobutton_'+str(radiovar))
        texttoset = str(currentradio.cget('text'))
        print(texttoset)

        labeltext = self.builder.get_variable('labeltext')
        labeltext.set(texttoset)

    def caller(self, name):
        print('naciśnięto ' + name)


if __name__ == '__main__':
    root = tk.Tk()
    app = Myapp(root)
    root.mainloop()