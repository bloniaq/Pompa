import csv

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


with open('var_dict_delimi.csv', 'r', newline='\n') as file:
    reader = csv.DictReader(file, delimiter=';')
    for i in reader:
        # print(i)
        print('name : ' + i['name'])
        print('value : ' + i['value'])
        print('type i.value : ' + str(type(i['value'])))
        if not i['data_type'] == 'string':
            print('eval value : ' + str(eval(i['value'])))
            print('type eval value : ' + str(type(eval(i['value']))))
            value = i['value']
        else:
            value = '\"' + i['value'] + '\"'
        print('\n')
        expression = i['name'] + ' = Variables(\"' + \
            i['name'] + '\", ' + \
            value + ', \"' + \
            i['data_type'] + '\", ' + \
            i['is_correct'] + ', ' +\
            i['valid_list'] + ', ' +\
            i['dan_id'] + ', ' +\
            i['dan_dict'] + ', \"' +\
            i['func_to_adjust'] + '\", ' +\
            i['func_list'] + ', ' +\
            i['is_active'] + ', ' +\
            i['obj_to_advice'] + ', \"' +\
            i['advice'] + '\")'
        print(expression)
        exec(expression)
        append_to_list_expr = 'variables_list.append(' + i['name'] + ')'
        eval(append_to_list_expr)
        print('\n\n')
    print(variables_list)
    print(ksztalt.value)
    print(tryb_pracy.value)
    print(str(type(tryb_pracy.value)))
