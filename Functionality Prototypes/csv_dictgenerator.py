import csv


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


ksztalt = Variables(
    'ksztalt',
    'kolo',
    'string',
    True,
    ['var = \'kolo\'', 'var = \'prostokat\''],
    2,
    {'0': 'prostokat', '1': 'kolo'},
    'nazwa funkcji adjust',
    ['lista', 'funkcji'],
    True,
    ['lista', 'obiektów advice'],
    'treść porady dla wyboru ksztaltu pompowni')
uklad_pompowni = Variables(
    'uklad_pompowni',
    'optymalny',
    'string',
    True,
    ['var = \'jednorzedowy\'', 'var = \'optymalny\''],
    3,
    {'0': 'jednorzedowy', '1': 'optymalny'},
    'nazwa funkcji adjust',
    ['lista', 'funkcji'],
    True,
    ['lista', 'obiektów advice'],
    'treść porady dla wyboru układu pompowni')
tryb_pracy = Variables(
    'tryb_pracy',
    0,
    'int',
    True,
    ['type(var) is string', 'var == \'minimalizacja\' or var == \'optymalizacja\' or var == \'spradzenie\''],
    1,
    {'0': 'minimalizacja', '1': 'sprawdzenie', '2': 'optymalizacja'},
    'nazwa funkcji adjust',
    ['self.zmien_tryb()', 'lista', 'funkcji'],
    True,
    ['Frame_Tryb'],
    'treść wskazówki')
minimalna_wys = Variables(
    'minimalna_wys',
    0.0,
    'double',
    True,
    ['type(var) is double'],
    9,
    {},
    'nazwa funkcji adjust',
    ['lista', 'funkcji'],
    True,
    ['Label_Minimalna_wys'],
    'treść wskazówki')

variables_list = [tryb_pracy, ksztalt, uklad_pompowni, minimalna_wys]
fieldnames = [
    'name',
    'value',
    'data_type',
    'is_correct',
    'valid_list',
    'dan_id',
    'dan_dict',
    'func_to_adjust',
    'func_list',
    'is_active',
    'obj_to_advice',
    'advice']

with open('var_dict.csv', 'w', newline='\n') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames)

    writer.writeheader()
    for i in variables_list:
        writer.writerow({
            'name': i.name,
            'value': i.value,
            'data_type': i.data_type,
            'is_correct': i.is_correct,
            'valid_list': i.valid_list,
            'dan_id': i.dan_id,
            'dan_dict': i.dan_dict,
            'func_to_adjust': i.func_to_adjust,
            'func_list': i.func_list,
            'is_active': i.is_active,
            'obj_to_advice': i.obj_to_advice,
            'advice': i.advice})
