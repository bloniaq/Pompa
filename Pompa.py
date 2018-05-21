try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 
import pygubu


class Application:
    def __init__(self):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('GUI_Pygubu.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Toplevel_Main')

        builder.connect_callbacks(self)

        callbacks = {
            'zmien_tryb': self.zmien_tryb,
            'uwzgledniaj_zwg': self.uwzgledniaj_zwg,
            'ksztalt_wymiary': self.ksztalt_wymiary,
            'calculate': self.calculate
        }

        builder.connect_callbacks(callbacks)

        # default values definition
        ksztalt = self.builder.get_variable('ksztalt')
        ksztalt.set('kolo')

    def zmien_tryb(self):
        mode = self.builder.tkvariables.__getitem__('tryb_pracy').get()
        nbook = self.builder.get_object('Notebook_Dane')
        if mode == 'sprawdzenie':
            print('wykonuje ' + mode)
            nbook.tab(3, state='disabled')
            nbook.tab(4, state='disabled')
        elif mode == 'minimalizacja':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='disabled')
        elif mode == 'optymalizacja':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='normal')

    def uwzgledniaj_zwg(self):
        mode_zwg = self.builder.tkvariables.__getitem__('count_zwg').get()
        entry_zwg = self.builder.get_object('Entry_Woda_gruntowa')
        if mode_zwg:
            entry_zwg.configure(state='normal')
        else:
            entry_zwg.configure(state='disabled')

    def ksztalt_wymiary(self):
        current_ksztalt = self.builder.tkvariables.__getitem__('ksztalt').get()
        en_sr_pom = self.builder.get_object('Entry_Średnica_pompowni')
        en_dl_pom = self.builder.get_object('Entry_Dlugosc_pompowni')
        en_sz_pom = self.builder.get_object('Entry_Szerokosc_pompowni')
        if current_ksztalt == 'kolo':
            en_sr_pom.configure(state='normal')
            en_dl_pom.configure(state='disabled')
            en_sz_pom.configure(state='disabled')
        elif current_ksztalt == 'prostokat':
            en_sr_pom.configure(state='disabled')
            en_dl_pom.configure(state='normal')
            en_sz_pom.configure(state='normal')

    def calculate(self):
        print('uruchomiono przeliczanie')

    def quit(self):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
