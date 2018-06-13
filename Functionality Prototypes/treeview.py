try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu, os

class Myapp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"treeview.ui")
        builder.add_from_file(fpath)

        self.mainwindow = builder.get_object('Toplevel_1')
        self.tree = tree = builder.get_object('Treeview')

        builder.connect_callbacks(self)


    def run(self):
        self.mainwindow.mainloop()

    def add_point(self):
        print('uruchomiono funkcję add_point')
        entry_x = self.builder.get_object('Entry_x')
        val_x = entry_x.get()
        entry_y = self.builder.get_object('Entry_y')
        val_y = entry_y.get()
        itemid = self.tree.insert('', tk.END, text='Punkt', values=(val_x, val_y))
        print(itemid)

    def delete_point(self):
    	print('uruchomiono funkcję delete_point')


if __name__ == '__main__':
    app = Myapp()
    app.run()

