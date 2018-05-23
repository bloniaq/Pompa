try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu

class Variables():
    def __init__(self, value, declaration, dan_id, dan_dict, is_matter,
        conditions, relatives, description, command=None):
        self.value = value
        self.declaration = declaration
        self.dan_id = dan_id
        self.dan_dict = dan_dict
        self.is_matter = is_matter
        self.conditions = conditions
        self.command = command
        self.relatives = relatives
        self.description = description

    def __name__(self):
        return self


class Application():
    def __init__(self):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('GUI_Pygubu.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Toplevel_Main')
        self.filepath = builder.get_object('filepath')

        # lista zmiennych
        # struktura zmiennej:
        #   nazwa = [
        #       wartość,
        #       wskaźnik na wybór użytkownika,
        #       'id w pliku DAN',
        #       {wart z DAN: wart w aplikacji},
        #       czy brany pod uwage,
        #       [lista walidacyjna],
        #       [lista obietkóœ powiązanych],
        #       'treść wskazówki'
        #       ],
        #tryb_pracy = ['0',
        #        self.builder.get_variable('tryb_pracy'),
        #        '1',
        #        {'0': 'minimalizacja', '1': 'sprawdzenie', '2':
        #            'optymalizacja'},
        #        True,
        #        ['type(var) is string', 'var == \'minimalizacja\' or var == \'optymalizacja\' or var == \'spradzenie\''],
        #        ['Frame_Tryb'],
        #        'treść wskazówki']
        #ksztalt = [
        #       'kolo',
        #       self.builder.get_variable('ksztalt'),
        #       '2',
        #       {'0': 'prostokat', '1': 'kolo'},
        #       True,
        #       ['type(var) is string', 'var == \'prostokat\'', 'var ==\'kolo\''],
        #       ['Label_Ksztalt'],
        #       'treść wskazówki'
        #       ]
        #uklad_pompowni = [
        #       'optymalny',
        #       self.builder.get_variable('uklad_pompowni'),
        #       '3',
        #       {'0': 'jednorzedowy', '1': 'optymalny'},
        #       True,
        #       ['type(var) is string', 'var == \'jednorzedowy\'', 'var == \'optymalny\''],
        #       ['Label_Uklad_pomp'],
        #       'treść wskazówki'
        #       ]

        #variables = [
        #    tryb_pracy,
        #    ksztalt,
        #    uklad_pompowni,
        #    ]

        self.ksztalt = ksztalt = Variables('kolo', self.builder.get_variable('ksztalt'),
            '2', {'0': 'prostokat', '1': 'kolo'}, True, ['type(var) is string', 'var == \'prostokat\'', 'var ==\'kolo\''], ['Label_Ksztalt'], 'treść wskazówki', 'self.ksztalt_wymiary()')

        self.uklad_pompowni = uklad_pompowni = Variables('optymalny',
               self.builder.get_variable('uklad_pompowni'),
               '3',
               {'0': 'jednorzedowy', '1': 'optymalny'},
               True,
               ['type(var) is string', 'var == \'jednorzedowy\'', 'var == \'optymalny\''],
               ['Label_Uklad_pomp'],
               'treść wskazówki')

        self.tryb_pracy = tryb_pracy = Variables('0',
                self.builder.get_variable('tryb_pracy'),
                '1',
                {'0': 'minimalizacja', '1': 'sprawdzenie', '2':
                    'optymalizacja'},
                True,
                ['type(var) is string', 'var == \'minimalizacja\' or var == \'optymalizacja\' or var == \'spradzenie\''],
                ['Frame_Tryb'],
                'treść wskazówki', 'self.zmien_tryb()')
        self.liczba_pomp_rez = liczba_pomp_rez = Variables('optymalna',
                self.builder.get_variable('liczba_pomp_rez'),
                '4',
                {'1': 'minimalna', '2': 'optymalna', '3': 'bezpieczna'},
                True,
                ['type(var) is string'],
                ['Label_Wariant_rezerwa'],
                'treść wskazówki'
                )
        self.minimalna_wys = minimalna_wys = Variables(0.0,
                self.builder.get_variable('minimalna_wys'),
                '9',
                {},
                True,
                ['type(var) is double'],
                ['Label_Minimalna_wys'],
                'treść wskazówki'
                )

        self.rzedna_terenu = rzedna_terenu = Variables(0.0,
                self.builder.get_variable('rzedna_terenu'),
                '10',
                {},
                True,
                ['type(var) is double'],
                ['Label_Rzedna_terenu'],
                'treść wskazówki'
                )

        self.rzedna_wylotu = rzedna_wylotu = Variables(0.0,
                self.builder.get_variable('rzedna_wylotu'),
                '11',
                {},
                True,
                ['type(var) is double'],
                ['Label_Rzedna_wylotu'],
                'treść wskazówki'
                )

        self.variables = variables = [ksztalt, uklad_pompowni, tryb_pracy, liczba_pomp_rez, minimalna_wys, rzedna_terenu, rzedna_wylotu]

        builder.connect_callbacks(self)

        callbacks = {
            'zmien_tryb': self.zmien_tryb,
            'uwzgledniaj_zwg': self.uwzgledniaj_zwg,
            'ksztalt_wymiary': self.ksztalt_wymiary,
            'calculate': self.calculate,
            'wczytaj_dane': self.wczytaj_dane,
            'zapisz_dane': self.zapisz_dane,
            'info': self.info
        }

        builder.connect_callbacks(callbacks)

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
        print('wykonano zmien_tryb')

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
        print('wykonano ksztalt_wymiary')

    def calculate(self):
        print('uruchomiono przeliczanie')

    def quit(self):
        self.mainwindow.quit()

    def wczytaj_dane(self, event=None):
        path = self.filepath.cget('path')
        with open(path, 'r+') as file:
            print('otwarto plik ' + str(file))
            # rozpoznaj plik
            first_line = file.readline()
            if first_line[0] == '1' and first_line[1] == ')':
                print('plik danych generowany wersją 1.0 aplikacji')
                file.seek(0)
                print('\n\n\n')
                for line in file:
                    id_line, line_datas = line.split(')')
                    line_datas_list = line_datas.split()
                    stored_value = line_datas_list[0]
                    print(id_line + ') ' + stored_value)
                    for i in self.variables:
                        print('czy to ta zmienna o id ' + i.dan_id)
                        if id_line == i.dan_id:
                            # print('znalazłem zmienna ktorej moge cos przypsiac')
                            # print('wartosc przed przyspianiem: ' + i.value)
                            print('i value przed zmiana ' + str(type(i.value)))
                            if isinstance(i.value, str):
                                i.value = stored_value
                            else:
                                i.value = eval(stored_value)
                            print('i value po zmianie ' + str(type(i.value)))
                            # print('i value = ' + i.value + ' <- to przypisano')
                            # print('stored value = ' + stored_value + ' <- z tego') 
                            for j in i.dan_dict:
                                # print('czy to ten klucz: ' + j)
                                # print('miałby taka wartość: ' + i.dan_dict[j])
                                if i.value == j or i.value is j:
                                    # print('znalazłem klucz')
                                    i.value = i.dan_dict[j]
                            i.declaration.set(i.value)
                            if i.command != None:
                                print('oho, bedzie funkcja moze ' + i.command)
                                eval(i.command)
                            break
                print('\n\n\n')
            # tutaj wstawic elif i warunek na nowa wersje

    def zapisz_dane(self):
        print('zapisz dane')

    def info(self):
        print('info')
        print('wartosc to ' + str(self.ksztalt.__name__))
        for i in self.variables:
            print(i.value + i.description)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
