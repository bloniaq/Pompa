try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu, csv, logging


variables_list = []

# LOGGING CONFIGURATION

# clearing root logger handlers
log = logging.getLogger()
log.handlers = []

# setting new logger
log = logging.getLogger('Pompa/main')
log.setLevel(logging.DEBUG)

# create console and file handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('logfile.log', 'w')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s', datefmt='%Y.%m.%d %H:%M:%S')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)
log.addHandler(fh)


class Variables():
    _items = {}

    def __init__(
        self, name, value, data_type, is_repr, unit, is_active, outcome_func,
            val_to_cvar, controlvar, load_func, load_func_args, dan_id,
            cvar_to_val, is_correct, valid_func, valid_func_args, adv_widgets,
            adv_content):
        self.name = name
        self.value = value
        self.data_type = data_type
        self.is_repr = is_repr
        self.unit = unit
        self.is_active = is_active
        self.outcome_func = outcome_func
        self.val_to_cvar = val_to_cvar
        self.controlvar = controlvar
        self.load_func = load_func
        self.load_func_args = load_func_args
        self.dan_id = dan_id
        self.cvar_to_val = cvar_to_val
        self.is_correct = is_correct
        self.valid_func = valid_func
        self.valid_func_args = valid_func_args
        self.adv_widgets = adv_widgets
        self.adv_content = adv_content

    def __repr__(self):
        return self.name

    def validate(self):
        log.info('validation of {0}'.format(self.name))
        return True

    def set_value(self, app_class):
        exec('app_class.' + self.val_to_cvar + '(self)')

    def run_outcome_func(self, app_class):
        exec('app_class.' + self.outcome_func + '()')


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
                '''
                expression = 'self.{0} = Variables(\"{0}\", {1}, \"{2}\", {3},\
                {4}, {5}, \"{6}\", \"{7}\", \"{8}\", \"{9}\", {10}, {11}, \
                \"{12}\", {13}, {14}, \"{15}\"\
                '''
                expression = 'self.{0} = Variables(\
\"{0}\", \
{1}, \
\"{2}\", \
{3}, \
{4}, \
{5}, \
\"{6}\", \
\"{7}\", \
\"{8}\", \
\"{9}\", \
\"{10}\", \
{11}, \
\"{12}\", \
{13}, \
\"{14}\", \
{15}, \
{16}, \
\"{17}\"\
)'.format(
                    i['name'],                      # 0
                    value,                          # 1
                    i['data_type'],                 # 2
                    i['is_repr'],                   # 3
                    i['unit'],                      # 4
                    i['is_active'],                 # 5
                    i['outcome_func'],              # 6
                    i['val_to_cvar'],               # 7
                    i['controlvar'],                # 8
                    i['load_func'],                 # 9
                    i['load_func_args'],            # 10
                    i['dan_id'],                    # 11
                    i['cvar_to_val'],               # 12
                    i['is_correct'],                # 13
                    i['valid_func'],                # 14
                    i['valid_func_args'],           # 15
                    i['adv_widgets'],               # 16
                    i['adv_content'])               # 17
                log.debug('\n{0}\n\n'.format(expression))
                exec(expression)
                append_to_list_expr = 'variables_list.append(self.' + \
                    i['name'] + ')'
                eval(append_to_list_expr)
            log.info('\n{0}\n\n'.format(variables_list))

        # 6: Setting default values in application
        for i in variables_list:
            if i.val_to_cvar != "":
                i.set_value(self)
            if i.outcome_func != "":
                i.run_outcome_func(self)

    # VAL TO CVAR FUNCTIONS

    def rewrite_to_cvar(self, variable):
        gui_variable = self.builder.get_variable(variable.controlvar)
        log.debug('\n\n{0}, {1}'.format(variable, type(variable.value)))
        gui_variable.set(variable.value)

    def res_to_cvar(self, variable):
        gui_variable = self.builder.get_variable(variable.controlvar)
        res_string = ""
        log.debug('\n\n')
        for i in variable.value:
            log.debug(i)
            res_string += str(i) + ', '
        res_string = res_string[:-2]
        log.debug('\nres string : {0}'.format(res_string))
        log.debug('{0}, {1}'.format(variable, "res string", type(res_string)))
        gui_variable.set(res_string)

    # DATA MANAGEMENT FUNCTIONS

    def wczytaj_dane(self, event=None):
        path = self.filepath.cget('path')
        with open(path, 'r+') as file:
            log.info('otwarto plik ' + str(file))
            # rozpoznaj plik
            first_line = file.readline()
            # rozpoznanie wersji zapisu
            if first_line[0] == '1' and first_line[1] == ')':
                log.info('plik danych generowany wersją 1.0 aplikacji')
                file.seek(0)
                log.info('\n\n\n')
                for line in file:
                    id_line, line_datas = line.split(')')
                    line_datas_list = line_datas.split()
                    stored_value = line_datas_list[0]
                    log.info(id_line + ') ' + stored_value)
                    for i in variables_list:
                        log.debug('czy to ta zmienna o id ' + str(i.dan_id))
                        if id_line == i.dan_id:
                            # print('wartosc przed przyspianiem: ' + i.value)
                            log.info('i value przed zmiana ' + str(type(i.value)))
                            if isinstance(i.value, str):
                                i.value = stored_value
                            else:
                                i.value = eval(stored_value)
                            log.info('i value po zmianie ' + str(type(i.value)))
                            for j in i.dan_dict:
                                # print('czy to ten klucz: ' + j)
                                if i.value == j or i.value is j:
                                    # print('znalazłem klucz')
                                    i.value = i.dan_dict[j]
                            i.declaration.set(i.value)
                            if i.command is not None:
                                log.debug('oho, bedzie funkcja moze ' + i.command)
                                eval(i.command)
                            break
                log.info('\n\n\n')
            # tutaj wstawic elif i warunek na nowa wersje

    def zapisz_dane(self):
        log.info('zapisz dane')

    # LOAD FUNCTIONS

    def handle_pump_char(self, variable):
        loaded_dict = {}
        for i in loaded_dict:
            self.pump_add_point(variable.value[i][0], variable.value[i][1])

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
        log.info('changed mode: {0}'.format(mode))

    def uwzgledniaj_zwg(self):
        mode_zwg = self.builder.tkvariables.__getitem__('count_zwg').get()
        entry_zwg = self.builder.get_object('Entry_Woda_gruntowa')
        if mode_zwg:
            entry_zwg.configure(state='normal')
        else:
            entry_zwg.configure(state='disabled')

    def change_shape(self):
        current_shape = self.builder.tkvariables.__getitem__('ksztalt').get()
        en_sr_pom = self.builder.get_object('Entry_Srednica_pompowni')
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
        log.info('changed shape: {0}'.format(current_shape))

        # TREEVIEW MANAGEMENT

    def pump_get_coords(self):
        log.info('')
        log.info('uruchomiono funkcję get_coords')
        entry_q = self.builder.get_object('Entry_Wsp_q')
        val_q = entry_q.get()
        entry_q.delete(0, 'end')
        entry_h = self.builder.get_object('Entry_Wsp_h')
        val_h = entry_h.get()
        entry_h.delete(0, 'end')
        self.pump_add_point(val_q, val_h)

    def pump_add_point(self, qcoord, hcoord):
        log.info('pump_add_point BEGUN')
        qcoord = str(qcoord)
        hcoord = str(hcoord)
        itemid = self.tree.insert('', tk.END, text='Punkt',
                                  values=('1', float(qcoord.replace(',', '.')),
                                          float(hcoord.replace(',', '.'))))
        self.char_pompy.value[itemid] = (qcoord, hcoord)
        log.debug(self.char_pompy.value)
        self.pump_sort_points()

    def pump_sort_points(self):
        log.info('uruchomiono funkcję sort_points')
        log.debug('odnaleziono obiekt kolumny')
        xnumbers = [(self.tree.set(i, 'Column_q'), i)
                    for i in self.tree.get_children('')]
        log.debug('utworzono listę elementów')
        log.info(xnumbers)
        xnumbers.sort(key=lambda t: float(t[0]))

        for index, (val, i) in enumerate(xnumbers):
            self.tree.move(i, '', index)
            self.tree.set(i, 'Column_nr', value=str(index + 1))

    def pump_delete_point(self):
        log.info('')
        log.info('uruchomiono funkcję delete_point')
        deleted_id = self.tree.focus()
        if deleted_id != '':
            self.tree.delete(deleted_id)
            del self.char_pompy.value[deleted_id]
        log.debug(self.char_pompy.value)
        self.pump_sort_points()

    # def pump_flow_unit_conversion(self):

    # VALIDATION FUNCTIONS

    def validate_all(self):
        log.info('uruchomiono walidację')

    def validate_floats(self):
        log.info('zwalidowano - floats')

    # CALCULATE FUNCTION

    def calculate(self):
        log.info('uruchomiono przeliczanie')

    # ABOUT PROGRAM FUNCTION

    def info(self):
        log.info('info')
        log.info('wartosc to ' + str(self.ksztalt.__name__))
        for i in self.variables:
            log.debug(i.value + i.description)

    def quit(self):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':

    app = Application()
    app.run()
