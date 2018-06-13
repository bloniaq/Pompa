try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu, os


class Myapp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__), "editabletreeview.ui")
        builder.add_from_file(fpath)
        self.pump_characteristic = {}

        self.mainwindow = builder.get_object('Toplevel_1')
        self.tree = builder.get_object('Treeview')

        # setting first column #0 width
        self.tree.heading('#0', text='id')
        self.tree.column('#0', minwidth=20, width=40, stretch=False)

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def add_point(self, xcoord, ycoord):
        print('uruchomiono funkcję add_point')
        itemid = self.tree.insert('', tk.END, text='Punkt',
                                  values=(xcoord, ycoord))
        self.pump_characteristic[itemid] = (eval(xcoord), eval(ycoord))
        print(self.pump_characteristic)
        self.sort_points()

    def sort_points(self):
        print('uruchomiono funkcję sort_points')
        print('odnaleziono obiekt kolumny')
        xnumbers = [(self.tree.set(i, 'Column_x'), i)
                    for i in self.tree.get_children('')]
        print('utworzono listę elementów')
        print(xnumbers)
        xnumbers.sort(key=lambda t: float(t[0]))

        for index, (val, i) in enumerate(xnumbers):
            self.tree.move(i, '', index)

    def get_coords(self):
        print('')
        print('uruchomiono funkcję get_coords')
        entry_x = self.builder.get_object('Entry_x')
        val_x = entry_x.get()
        entry_y = self.builder.get_object('Entry_y')
        val_y = entry_y.get()
        self.add_point(val_x, val_y)

    def delete_point(self):
        print('')
        print('uruchomiono funkcję delete_point')
        deleted_id = self.tree.focus()
        if deleted_id != '':
            self.tree.delete(deleted_id)
            del self.pump_characteristic[deleted_id]
        print(self.pump_characteristic)


if __name__ == '__main__':
    app = Myapp()
    app.run()

