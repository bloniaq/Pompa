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

# ANOTHER LINES

        callbacks = {
            'uwzgledniaj_zwg': self.uwzgledniaj_zwg,
            'calculate': self.calculate,
            'wczytaj_dane': self.wczytaj_dane,
            'zapisz_dane': self.zapisz_dane,
            'info': self.info
        }

        builder.connect_callbacks(callbacks)

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
