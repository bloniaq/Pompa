import sys
import os

try:
    import tkinter as tk
except:
    import Tkinter as tk

import pygubu

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


class Variables():
    def __init__(self, value, obj_id, adv_content):
        self.value = value
        self.obj_id = obj_id
        self.adv_content = adv_content


class Myapp:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__), "advice.ui")
        builder.add_from_file(fpath)

        mainwindow = builder.get_object('Frame_1', master)

        builder.connect_callbacks(self)

        callbacks = {
            'Advice_for_Entry_1': self.Advice_for_Entry_1
        }

        builder.connect_callbacks(callbacks)

        self.variable_1 = variable_1 = Variables(
            19.16,
            'Entry_1',
            'advice text for entry_1'
        )

        self.variable_2 = variable_2 = Variables(
            4.20,
            'Entry_2',
            'advice text for entry_2'
        )

        self.variable_3 = variable_3 = Variables(
            1899,
            'Entry_3',
            'advice text for entry_3'
        )

        self.variables_list = [variable_1, variable_2, variable_3]

    def Show_advice(self, event, widget_id):
        advice_variable = self.builder.get_variable('advice_text')
        for i in self.variables_list:
            if widget_id == i.obj_id:
                suitable_advice = i.adv_content
                break
        advice_variable.set(suitable_advice)
        print('Advice for ' + i.obj + ' is showed')

    def Advice_for_Entry_1(self, event):
        advice_variable = self.builder.get_variable('advice_text')
        suitable_advice = self.variable_1.adv_content
        advice_variable.set(suitable_advice)
        print('This simpliest way for Entry 1 obviously works')


if __name__ == '__main__':
    root = tk.Tk()
    app = Myapp(root)
    root.mainloop()
