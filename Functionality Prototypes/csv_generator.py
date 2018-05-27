import csv


class Variables():
    def __init__(
        self, ident, value, data_type, is_correct, valid_list, dan_id,
            dan_dict, is_active, advice):
        self.ident = ident
        self.value = value
        self.data_type = data_type
        self.is_correct = is_correct
        self.valid_list = valid_list
        self.dan_id = dan_id
        self.dan_dict = dan_dict
        self.is_active = is_active
        self.advice = advice


ksztalt = Variables(
    'ksztalt',
    'kolo',
    'string',
    True,
    ['var = \'kolo\'', 'var = \'prostokat\''],
    2,
    {'0': 'prostokat', '1': 'kolo'},
    True,
    'treść porady dla wyboru ksztaltu pompowni')
uklad_pompowni = Variables(
    'uklad_pompowni',
    'optymalny',
    'string',
    True,
    ['var = \'jednorzedowy\'', 'var = \'optymalny\''],
    3,
    {'0': 'jednorzedowy', '1': 'optymalny'},
    True,
    'treść porady dla wyboru układu pompowni')

variables_list = [ksztalt, uklad_pompowni]

with open('var_data.csv', 'w', newline='\n') as file:
    write = csv.writer(file, delimiter=' ', quotechar='|')
    write.writerow(['ident', 'value', 'data_type', 'is_correct'])
    for i in variables_list:
        write.writerow([i.ident, i.value, i.data_type, i.is_correct])
