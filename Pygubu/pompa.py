#test.py
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu


class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('GUI_Pygubu.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Frame_Main', master)

    def modesss (self):
        print('jebac')
        mode = self.builder.get_variable('mode')
        print (str(mode))
        if mode == 1:
            print("chuj")
    def calculate(self):
        print('calculate')
        messagebox.showinfo('Chuj')




if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
