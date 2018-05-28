import csv


variables_list = []


class Variables():
    def __init__(
        self, ident, value, data_type, is_correct):
        self.ident = ident
        self.value = value
        self.data_type = data_type
        self.is_correct = is_correct

with open('var_data.csv', 'r', newline='\n') as file:
    reader = csv.reader(file, delimiter=' ')
    headers = reader.__next__()
    for i in reader:
        expression = i[0] + ' = Variables(\"' + i[0] + '\", \"' + i[1] + '\", \"' + i[2] + '\", ' + i[3] + ')'
        print(expression)
        exec(expression)
        variables_list.append(expression)
        # append_to_list_expr = 'variables_list.append(' + i[0] + ')'
        # eval(append_to_list_expr)
    print(headers)
    print(variables_list)
    print(ksztalt.value)