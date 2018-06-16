try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu, csv


variables_list = []


class Variables():
    def __init__(
        self, name, value, data_type, is_correct, valid_list, dan_id,
            dan_dict, func_to_adjust, func_list, is_active, obj_to_advice,
            advice):
        self.name = name
        self.value = value
        self.data_type = data_type
        self.is_correct = is_correct
        self.valid_list = valid_list
        self.dan_id = dan_id
        self.dan_dict = dan_dict
        self.func_to_adjust = func_to_adjust
        self.func_list = func_list
        self.is_active = is_active
        self.obj_to_advice = obj_to_advice
        self.advice = advice

    def __repr__(self):
        return self.name

    def validate(self):
        print('validation of ' + self.name)
        return True

    def set_value(self, app_class):
        gui_variable = app_class.builder.get_variable(self.name)
        gui_variable.set(self.value)

    def run_func_list(self, app_class):
        for func in self.func_list:
            exec('app_class.' + func)


class Application():
    def __init__(self):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('GUI_Pygubu.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('Toplevel_Main')
        self.filepath = builder.get_object('filepath')
        self.tree = builder.get_object('Treeview_Pump')
        self.pump_characteristic = {}
        self.punkty_pompy = {}

        # 4: Setting callbacks
        builder.connect_callbacks(self)

        '''
        callbacks = {
            'uwzgledniaj_zwg': self.uwzgledniaj_zwg,
            'calculate': self.calculate,
            'wczytaj_dane': self.wczytaj_dane,
            'zapisz_dane': self.zapisz_dane,
            'info': self.info
        }

        builder.connect_callbacks(callbacks)
        '''

        # 5: Loading variables form a csv file
        with open('variables.csv', 'r', newline='\n') as file:
            reader = csv.DictReader(file, delimiter=';')
            for i in reader:
                # print('name : ' + i['name'])
                # print('value : ' + i['value'])
                # print('type i.value : ' + str(type(i['value'])))
                if not i['data_type'] == 'string':
                    # print('eval value : ' + str(eval(i['value'])))
                    # print('type eval value : ' + str(type(eval(i['value']))))
                    value = i['value']
                else:
                    value = '\"' + i['value'] + '\"'
                # print('\n')
                expression = 'self.{0} = Variables(\"{0}\", {1}, \"{2}\", {3},\
                    {4}, {5}, {6}, \"{7}\", {8}, {9}, {10}, \"{11}\")'\
                    .format(i['name'], value, i['data_type'], i['is_correct'],
                            i['valid_list'], i['dan_id'], i['dan_dict'],
                            i['func_to_adjust'], i['func_list'],
                            i['is_active'], i['obj_to_advice'], i['advice'])
                print(expression)
                exec(expression)
                append_to_list_expr = 'variables_list.append(self.' + \
                    i['name'] + ')'
                eval(append_to_list_expr)
            # print(variables_list)
            # print(self.ksztalt.value)
            # print(self.tryb_pracy.value)
            # print(str(type(self.tryb_pracy.value)))

        # 6: Setting default values in application
        for i in variables_list:
            i.set_value(self)
            i.run_func_list(self)

    # DATA MANAGEMENT FUNCTIONS

    def wczytaj_dane(self, event=None):
        path = self.filepath.cget('path')
        with open(path, 'r+') as file:
            print('otwarto plik ' + str(file))
            # rozpoznaj plik
            first_line = file.readline()
            # rozpoznanie wersji zapisu
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
                            # print('wartosc przed przyspianiem: ' + i.value)
                            print('i value przed zmiana ' + str(type(i.value)))
                            if isinstance(i.value, str):
                                i.value = stored_value
                            else:
                                i.value = eval(stored_value)
                            print('i value po zmianie ' + str(type(i.value)))
                            for j in i.dan_dict:
                                # print('czy to ten klucz: ' + j)
                                if i.value == j or i.value is j:
                                    # print('znalazłem klucz')
                                    i.value = i.dan_dict[j]
                            i.declaration.set(i.value)
                            if i.command is not None:
                                print('oho, bedzie funkcja moze ' + i.command)
                                eval(i.command)
                            break
                print('\n\n\n')
            # tutaj wstawic elif i warunek na nowa wersje

    def zapisz_dane(self):
        print('zapisz dane')

    # INTERNAL FUNCTIONS

    def change_mode(self):
        ''' changes application mode
        '''
        mode = self.builder.tkvariables.__getitem__('tryb_pracy').get()
        nbook = self.builder.get_object('Notebook_Dane')
        if mode == 'sprawdzenie':
            nbook.tab(3, state='disabled')
            nbook.tab(4, state='disabled')
        elif mode == 'minimalizacja':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='disabled')
        elif mode == 'optymalizacja':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='normal')
        print('changed mode:', mode)

    def uwzgledniaj_zwg(self):
        mode_zwg = self.builder.tkvariables.__getitem__('count_zwg').get()
        entry_zwg = self.builder.get_object('Entry_Woda_gruntowa')
        if mode_zwg:
            entry_zwg.configure(state='normal')
        else:
            entry_zwg.configure(state='disabled')

    def change_shape(self):
        current_shape = self.builder.tkvariables.__getitem__('ksztalt').get()
        en_sr_pom = self.builder.get_object('Entry_Średnica_pompowni')
        en_dl_pom = self.builder.get_object('Entry_Dlugosc_pompowni')
        en_sz_pom = self.builder.get_object('Entry_Szerokosc_pompowni')
        if current_shape == 'kolo':
            en_sr_pom.configure(state='normal')
            en_dl_pom.configure(state='disabled')
            en_sz_pom.configure(state='disabled')
        elif current_shape == 'prostokat':
            en_sr_pom.configure(state='disabled')
            en_dl_pom.configure(state='normal')
            en_sz_pom.configure(state='normal')
        print('setting shape:', current_shape)

        # TREEVIEW MANAGEMENT

    def pump_get_coords(self):
        print('')
        print('uruchomiono funkcję get_coords')
        entry_q = self.builder.get_object('Entry_Wsp_q')
        val_q = entry_q.get()
        entry_q.delete(0, 'end')
        entry_h = self.builder.get_object('Entry_Wsp_h')
        val_h = entry_h.get()
        entry_h.delete(0, 'end')
        self.pump_add_point(val_q, val_h)

    def pump_add_point(self, qcoord, hcoord):
        print('pump_add_point BEGUN')
        itemid = self.tree.insert('', tk.END, text='Punkt',
                                  values=('1', float(qcoord.replace(',', '.')),
                                          float(hcoord.replace(',', '.'))))
        self.pump_characteristic[itemid] = (qcoord, hcoord)
        print(self.pump_characteristic)
        self.pump_sort_points()

    def pump_sort_points(self):
        print('uruchomiono funkcję sort_points')
        print('odnaleziono obiekt kolumny')
        xnumbers = [(self.tree.set(i, 'Column_q'), i)
                    for i in self.tree.get_children('')]
        print('utworzono listę elementów')
        print(xnumbers)
        xnumbers.sort(key=lambda t: float(t[0]))

        for index, (val, i) in enumerate(xnumbers):
            self.tree.move(i, '', index)
            self.tree.set(i, 'Column_nr', value=str(index + 1))

    def pump_delete_point(self):
        print('')
        print('uruchomiono funkcję delete_point')
        deleted_id = self.tree.focus()
        if deleted_id != '':
            self.tree.delete(deleted_id)
            del self.pump_characteristic[deleted_id]
        print(self.pump_characteristic)
        self.pump_sort_points()

    # def pump_flow_unit_conversion(self):

    # VALIDATION FUNCTIONS

    def validate_all(self):
        print('uruchomiono walidację')

    def validate_floats(self):
        print('zwalidowano - floats')

    # CALCULATE FUNCTION

    def calculate(self):
        print('uruchomiono przeliczanie')

    # ABOUT PROGRAM FUNCTION

    def info(self):
        print('info')
        print('wartosc to ' + str(self.ksztalt.__name__))
        for i in self.variables:
            print(i.value + i.description)

    def quit(self):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
