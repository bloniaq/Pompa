try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python
import pygubu, csv, logging, copy

variables_list = []
path = ""

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
formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s',
                              datefmt='%Y.%m.%d %H:%M:%S')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)
log.addHandler(fh)


class Variables():

    def __init__(
        self, name, value, data_type, is_repr, unit, is_active, outcome_func,
            val_to_cvar, controlvar, load_func, load_func_args, dan_id,
            cvar_to_val, is_correct, valid_func, valid_func_args, adv_widgets,
            adv_content, app_instance):
        self.name = name
        self.value = value
        self.data_type = data_type
        self.is_repr = is_repr
        self.unit = unit
        self.is_active = is_active
        if outcome_func != "":
            self.outcome_func = eval('app_instance.{}'.format(outcome_func))
        else:
            self.outcome_func = None
        if val_to_cvar != "":
            self.val_to_cvar = eval('app_instance.{}'.format(val_to_cvar))
        else:
            self.val_to_cvar = None
        self.controlvar = controlvar
        if load_func != '':
            self.load_func = eval('app_instance.{}'.format(load_func))
        else:
            self.load_func = None
        self.load_func_args = load_func_args
        self.dan_id = dan_id
        self.cvar_to_val = cvar_to_val
        self.is_correct = is_correct
        self.valid_func = valid_func
        self.valid_func_args = valid_func_args
        self.adv_widgets = adv_widgets
        self.adv_content = adv_content
        self.test_attr = load_func

    def __repr__(self):
        return self.name

    def validate(self):
        log.info('validation of {0}'.format(self.name))
        return True

    def set_value(self, app_class):
        if self.val_to_cvar is not None:
            self.val_to_cvar(self)

    def run_outcome_func(self, app_class):
        if self.outcome_func is not None:
            self.outcome_func()


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
                if not i['data_type'] == 'string':
                    value = i['value']
                else:
                    value = '\"' + i['value'] + '\"'
                if not i['load_func_args'] == '':
                    load_func_args = eval(i['load_func_args'])
                    log.debug('load func args: {}'.format(load_func_args))
                else:
                    load_func_args = None
                # Expression construction
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
{10}, \
{11}, \
\"{12}\", \
{13}, \
\"{14}\", \
{15}, \
{16}, \
\"{17}\", \
self\
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
                    load_func_args,                 # 10
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
            log.debug('test_attr: {}'.format(i.test_attr))
            log.debug('load_func: {}'.format(i.load_func))

        # 7: Binding advices content
        self.bind_advices()

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

    def bind_val_with_cvar(self, variable):
        log.debug('bind_val_with_cvar started')
        gui_variable = self.builder.get_variable(variable.controlvar)
        gui_variable.set(variable.value)

    # DATA MANAGEMENT FUNCTIONS

    def data_load(self):
        log.info('\ndata_load started\n')
        global path
        path = self.filepath.cget('path')
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n\n'.format(str(file)))
            # rozpoznaj plik
            first_line = file.readline()
            # rozpoznanie wersji zapisu
            if first_line[0] == '1' and first_line[1] == ')':
                self.dan_load(path)

    def dan_load(self, path):
        log.info('\ndan_load started\n')
        log.info('plik danych generowany wersją 1.0 aplikacji')
        self.builder.tkvariables.__getitem__('doplyw_jednostka').set(1)
        self.builder.tkvariables.__getitem__('wydajnosc_do').set(1)
        self.builder.tkvariables.__getitem__('wydajnosc_od').set(1)
        self.builder.tkvariables.__getitem__('char_pompy_jednostka').set(1)
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n\n'.format(str(file)))
            for line in file:
                id_line, line_datas = line.split(')')
                line_datas_list = line_datas.split()
                stored_value = line_datas_list[0]
                log.debug('dan_id: {0}) {1} <-readed_value'.format(
                    id_line, stored_value))
                log.debug('type id_line: {0}'.format(type(id_line)))
                for i in variables_list:
                    if i.load_func is None:
                        continue
                    if eval(id_line) == i.dan_id:
                        l_to_skip = i.load_func(i, stored_value,
                                                i.load_func_args)
                        log.info('i.load_func {0} executed,\
                            returned {1}'.format(
                            i.test_attr, l_to_skip))
                        for _ in range(l_to_skip):
                            next(file)
                        break

    # LOAD FUNCTIONS

    def dict_dan_to_val(self, obj, value, dictionary):
        log.info('\ndict_dan_to_val started\n')
        translated_value = dictionary[str(value)]
        log.debug('translated_value: {0}'.format(translated_value))
        obj.value = translated_value
        obj.set_value(self)
        log.debug('{0}.value changed to {1}'.format(obj, translated_value))
        if obj.outcome_func != "":
            obj.run_outcome_func(self)
        log.info('\nvalue set, function ended\n\n\n')
        return 0

    def rewrite_dan_to_val(self, obj, value, *args):
        log.info('\nrewrite_dan_to_val started\n')
        obj.value = eval(value)
        obj.unit = 1
        if obj.val_to_cvar != "":
            obj.set_value(self)
        log.debug('{0}.value changed to {1}'.format(obj, value))
        if obj.outcome_func != "":
            obj.run_outcome_func(self)
        log.info('\nvalue set, function ended\n\n\n')
        return 0

    def handle_loc_res(self, obj, value, *args):
        log.info('\nhandle_loc_res started\n')
        global path
        obj.value = []
        res_counter = 0
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n'.format(str(file)))
            for line in file:
                id_line, line_datas = line.split(')')
                line_datas_list = line_datas.split()
                if eval(id_line) < obj.dan_id - 1:
                    continue
                elif eval(id_line) == obj.dan_id - 1:
                    res_counter = eval(line_datas_list[0])
                elif eval(id_line) == obj.dan_id:
                    obj.value.append(line_datas_list[0])
                elif eval(id_line) > obj.dan_id:
                    continue
            obj.val_to_cvar(obj)
        log.info('handle_loc_res func ended\n\n')
        return res_counter - 1

    def handle_pump_char(self, obj, value, *args):
        log.info('\nhandle_pump_char\n')
        global path
        actual_id_list = []
        for i in obj.value.keys():
            actual_id_list.append(i)
        for j in actual_id_list:
            self.pump_delete_point(j)
        q_list = []
        h_list = []
        obj.unit = 1
        res_counter = 0
        with open(path, 'r+') as file:
            log.info('opening file: {0}\n'.format(str(file)))
            for line in file:
                id_line, line_datas = line.split(')')
                line_datas_list = line_datas.split()
                if eval(id_line) < obj.dan_id - 1:
                    continue
                elif eval(id_line) == obj.dan_id - 1:
                    res_counter = 2 * eval(line_datas_list[0])
                elif eval(id_line) == obj.dan_id:
                    q_list.append(eval(line_datas_list[0]))
                elif eval(id_line) == obj.dan_id + 1:
                    h_list.append(eval(line_datas_list[0]))
                elif eval(id_line) > obj.dan_id + 1:
                    continue
        log.debug('q_list: {}'.format(q_list))
        log.debug('h_list: {}'.format(h_list))
        for i in range(len(q_list)):
            self.pump_add_point(q_list[i], h_list[i])
        return res_counter - 1

    # INTERNAL FUNCTIONS

    def uwzgledniaj_zwg(self):
        mode_zwg = self.builder.tkvariables.__getitem__('count_zwg').get()
        entry_zwg = self.builder.get_object('Entry_Woda_gruntowa')
        if mode_zwg:
            entry_zwg.configure(state='normal')
        else:
            entry_zwg.configure(state='disabled')

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
        self.char_pompy.value[itemid] = (eval(qcoord), eval(hcoord))
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

    def pump_delete_button(self):
        log.info('pump_delete_button started')
        deleted_id = self.tree.focus()
        if deleted_id != '':
            self.pump_delete_point(deleted_id)

    def pump_delete_point(self, id_to_delete):
        log.info('uruchomiono funkcję delete_point')
        log.debug('point to delete: {}'.format(
            self.char_pompy.value[id_to_delete]))
        del self.char_pompy.value[id_to_delete]
        self.tree.delete(id_to_delete)
        log.debug('actual dict: {}'.format(self.char_pompy.value))
        self.pump_sort_points()

    # CONVERSION FUNCTIONS

    def control_inflow_unit(self):
        log.info('control_inflow_unit started')
        current_setting = self.builder.tkvariables.__getitem__(
            'doplyw_jednostka').get()
        if current_setting != self.doplyw_max.unit:
            self.change_inflow_unit(current_setting)

    def change_inflow_unit(self, current_setting):
        log.info('change_inflow_unit started')
        log.debug('current setting passed: {}'.format(current_setting))
        if current_setting == 1:
            self.doplyw_max.value = self.doplyw_max.value / 3.6
            self.doplyw_max.value = round(self.doplyw_max.value, 2)
            self.doplyw_min.value = self.doplyw_min.value / 3.6
            self.doplyw_min.value = round(self.doplyw_min.value, 2)
        elif current_setting == 2:
            self.doplyw_max.value = self.doplyw_max.value * 3.6
            self.doplyw_max.value = round(self.doplyw_max.value, 2)
            self.doplyw_min.value = self.doplyw_min.value * 3.6
            self.doplyw_min.value = round(self.doplyw_min.value, 2)
        self.doplyw_min.unit = current_setting
        self.doplyw_max.unit = current_setting
        self.doplyw_max.val_to_cvar(self.doplyw_max)
        self.doplyw_min.val_to_cvar(self.doplyw_min)

    def control_pump_flow_unit(self):
        log.info('control_pump_flow_unit started')
        current_setting = self.builder.tkvariables.__getitem__(
            'char_pompy_jednostka').get()
        if current_setting != self.char_pompy.unit:
            self.change_char_pompy_unit(current_setting)

    def change_char_pompy_unit(self, current_setting):
        log.info('change_char_pompy_unit started')
        log.debug('current setting passed: {}'.format(current_setting))
        key_list = []
        for key in self.char_pompy.value.keys():
            key_list.append(key)
        temp_dict = copy.deepcopy(self.char_pompy.value)
        log.debug('current dict_value: {}'.format(self.char_pompy.value))
        log.debug('current temp_dict: {}'.format(temp_dict))
        log.debug('current key_list: {}'.format(key_list))
        for key in key_list:
            log.debug('start delete dict loop')
            self.pump_delete_point(key)
        log.debug('current dict_value: {}'.format(self.char_pompy.value))
        log.debug('current temp_dict: {}'.format(temp_dict))
        log.debug('current key_list: {}'.format(key_list))
        if current_setting == 1:
            self.wydajnosc_od.value /= 3.6
            self.wydajnosc_do.value /= 3.6
            unit_text = '[l/s]'
            self.builder.tkvariables.__getitem__('wsp_q_text').set(
                'Przepływ Q {}'.format(unit_text))
            self.builder.tkvariables.__getitem__('wydajnosc_od_text').set(
                'Od {}'.format(unit_text))
            self.builder.tkvariables.__getitem__('wydajnosc_do_text').set(
                'Do {}'.format(unit_text))
            for key in temp_dict.keys():
                conv_flow = temp_dict[key][0] / 3.6
                conv_flow = round(conv_flow, 2)
                self.pump_add_point(conv_flow, temp_dict[key][1])
        elif current_setting == 2:
            self.wydajnosc_od.value *= 3.6
            self.wydajnosc_do.value *= 3.6
            unit_text = '[m³/h]'
            self.builder.tkvariables.__getitem__('wsp_q_text').set(
                'Przepływ Q {}'.format(unit_text))
            self.builder.tkvariables.__getitem__('wydajnosc_od_text').set(
                'Od {}'.format(unit_text))
            self.builder.tkvariables.__getitem__('wydajnosc_do_text').set(
                'Do {}'.format(unit_text))
            for key in temp_dict.keys():
                conv_flow = temp_dict[key][0] * 3.6
                conv_flow = round(conv_flow, 2)
                self.pump_add_point(conv_flow, temp_dict[key][1])
        self.char_pompy.unit = current_setting
        self.wydajnosc_do.unit = current_setting
        self.wydajnosc_od.unit = current_setting
        self.wydajnosc_od.set_value(self)
        self.wydajnosc_do.set_value(self)

    # ADVICES

    def bind_advices(self):
        for variable in variables_list:
            for widget in variable.adv_widgets:
                handler = self.builder.get_object(widget)
                print(widget + ' rozpoznano obiekt')
                handler.bind(
                    '<Enter>', lambda e,
                    advice=variable.adv_content: self.Show_advice(e, advice))
                print('wpisano mu treść podpowiedzi')
                print(' ')

    def Show_advice(self, event, advice):
        advice_variable = self.builder.get_variable('advice_text')
        advice_variable.set(advice)
        print('Advice is showed')

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
        log.debug('obrys_pompy.value: {}'.format(self.obrys_pompy.value))
        log.debug('type obrys_pompy.value: {}'.format(type(
            self.obrys_pompy.value)))
        log.debug('obrys_pompy.var: {}'.format(
            self.builder.tkvariables.__getitem__('obrys_pompy').get()))
        log.debug('type obrys_pompy.value: {}'.format(type(
            self.builder.tkvariables.__getitem__('obrys_pompy').get())))

    def quit(self):
        self.mainwindow.quit()
