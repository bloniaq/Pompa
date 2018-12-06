import logging
import tkinter as tk  # for python 3

log = logging.getLogger('Pompa.variables')


class Variable():

    def __init__(self, app, ui_variable, dan_id):
        self.app = app
        self.builder = app.builder
        self.tkvars = app.builder.tkvariables
        self.dan_id = dan_id
        if ui_variable in self.tkvars:
            self.ui_var = self.tkvars.__getitem__(ui_variable)
        else:
            log.debug('No ui_variable named {}'.format(ui_variable))
        self.load_flag = False

    '''
    def set_trace(self, attr):
        self.ui_var.trace(
            'w', lambda *_: setattr(self, attr, self.ui_var.get())
        )
    '''

    def set_trace(self, attr):
        self.ui_var.trace(
            'w', lambda *_: self.alt_setattr(attr)
        )

    def alt_setattr(self, attr):
        try:
            ui_content = self.ui_var.get()
        except tk.TclError as e:
            log.error('Tkinter error {}'.format(e))
            pass
        else:
            setattr(self, attr, ui_content)
        if self.chart_req and not self.load_flag:
            try:
                self.app.draw_figure()
            except (AttributeError, TypeError) as e:
                log.error('Error {}'.format(e))

    def load_data(self, data_dict):
        self.load_flag = True
        if self.dan_id in data_dict:
            self.value = data_dict[self.dan_id]
        self.load_flag = False


class Numeric(Variable):
    """keeps rational numbers or integers and connect them with ui variables"""

    def __init__(self, app, value, ui_variable, dan_id, chart_req):
        self.chart_req = chart_req
        super().__init__(app, ui_variable, dan_id)
        self.value = value
        self.set_trace('value')

    def __repr__(self):
        try:
            output = 'Numeric({}, {}, {});{}'.format(
                self.app, self.value, self.dan_id, self.ui_var.get())
        except tk.TclError as e:
            output = 'Numeric({}, {}, {});ERROR:{}'.format(
                self.app, self.value, self.dan_id, e)
        return output


class P_Int(Numeric):
    def __init__(self, app, value, ui_variable, dan_id, chart_req=False):
        super().__init__(app, value, ui_variable, dan_id, chart_req)

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            self.__dict__['value'] = value
            self.ui_var.set(self.value)
            if self.chart_req and not self.load_flag:
                try:
                    self.app.draw_figure()
                except (AttributeError, TypeError) as e:
                    log.error('Error {}'.format(e))


class P_Float(Numeric):
    def __init__(self, app, value, ui_variable, dan_id, chart_req=False):
        super().__init__(app, value, ui_variable, dan_id, chart_req)

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            self.__dict__['value'] = float(value)
            if self.__dict__['value'] != float(self.ui_var.get()):
                self.ui_var.set(value)
            if self.chart_req and not self.load_flag:
                try:
                    self.app.draw_figure()
                except (AttributeError, TypeError) as e:
                    log.error('Error {}'.format(e))


class Logic(Variable):
    """keeps logic variables and connect them with ui variables"""

    def __init__(self, app, value, ui_variable, dan_id, dictionary, function,
                 chart_req=False):
        super().__init__(app, ui_variable, dan_id)
        self.function = function
        self.chart_req = chart_req
        self.dictionary = dictionary
        self.value = value
        self.set_trace('value')

    def __repr__(self):
        output = 'Logic({}, {}, {}, {});{}'.format(
            self.app, self.value, self.dan_id, self.dictionary,
            self.ui_var.get())
        return output

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value
        if attr == 'value' and self.ui_var.get() != self.value:
            if isinstance(value, int) or isinstance(value, float):
                value = str(int(value))
                self.__dict__['value'] = self.dictionary[value]
            else:
                self.__dict__['value'] = value
            self.ui_var.set(self.value)
            if self.function is not None:
                self.function()


class Resistance(Variable):
    """class for local resistance in pipes"""

    def __init__(self, app, string, ui_variable, dan_id, chart_req=True):
        super().__init__(app, ui_variable, dan_id)
        self.chart_req = chart_req
        self.string = string
        self.set_trace('string')

    def __repr__(self):
        output = 'Resistance({}, str:{}, val:{}, {});{}'.format(
            self.app, self.string, self.values, self.dan_id, self.ui_var.get())
        return output

    def __setattr__(self, attr, value):
        if attr != 'string':
            self.__dict__[attr] = value
        elif isinstance(value, float):
            self.__dict__['string'] = str(value)
            self.__dict__['values'] = [value]
        elif isinstance(value, str):
            self.__dict__['string'] = value
            log.debug('trying to convert: {} to floats list'.format(value))
            if value != '':
                self.__dict__['values'] = [float(s) for s in value.split(',')]
            else:
                self.__dict__['values'] = []
        elif isinstance(value, list):
            self.__dict__['values'] = value
            string = str(value[0])
            if len(value) > 1:
                for element in range(1, len(value)):
                    string += ', {}'.format(str(element))
            self.__dict__['string'] = string
        if attr == 'string' and self.string != self.ui_var.get():
            self.ui_var.set(self.string)

    def load_data(self, data_dict):
        self.load_flag = True
        if self.dan_id in data_dict:
            self.string = data_dict[self.dan_id]
        self.load_flag = False


class Flow(Variable):
    """class for flow"""

    def __init__(self, app, value, ui_variable, dan_id, unit_ui_var,
                 unit='meters', chart_req=False):
        super().__init__(app, ui_variable, dan_id)
        self.chart_req = chart_req
        self.unit_var = self.tkvars.__getitem__(unit_ui_var)
        self.value = value
        self.unit = unit
        self.unit_var.set(unit)
        if ui_variable in self.tkvars:
            self.set_trace('value')
        self.unit_var.trace('w', lambda *_: self.convert(self.unit_var.get()))
        self.value_meters = 0
        self.value_liters = 0

    def __repr__(self):
        output = 'Flow({}, {}, {}, {});{}'.format(
            self.app, self.value, self.dan_id, self.unit, self.ui_var.get())
        return output

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            self.__dict__['value'] = round(float(value), 3)
            self.get_both_vals(value, self.unit_var.get())
            if self.__dict__['value'] != self.ui_var.get():
                self.ui_var.set(self.value)
            if self.chart_req and not self.load_flag:
                try:
                    self.app.draw_figure()
                except (AttributeError, TypeError) as e:
                    log.error('Error {}'.format(e))

    def get_both_vals(self, value, unit):
        if unit == 'meters':
            self.value_meters = self.value
            self.value_liters = round(self.value / 3.6, 3)
        elif unit == 'liters':
            self.value_liters = self.value
            self.value_meters = round(self.value * 3.6, 3)

    def convert(self, new_unit):
        self.load_flag = True
        log.info('conversion func starts')
        log.info('old value: {}'.format(self.value))
        if new_unit == self.unit:
            log.info('no need to conversion')
            return
        elif new_unit == 'meters':
            self.unit = new_unit
            log.debug('{} * 3.6 = {}'.format(self.value, self.value * 3.6))
            self.value = self.value_meters
        elif new_unit == 'liters':
            self.unit = new_unit
            log.debug('{} / 3.6 = {}'.format(self.value, self.value / 3.6))
            self.value = self.value_liters
        log.info('new value: {}'.format(self.value))
        self.load_flag = False

    def load_data(self, data_dict):
        if self.dan_id in data_dict:
            self.unit_var.set('liters')
            super().load_data(data_dict)


class PumpCharFlow(Flow):

    def __init__(self, value, unit, ui_var):
        self.value = value
        self.unit = unit
        self.unit_var = ui_var
        self.value_meters = 0
        self.value_liters = 0
        self.get_both_vals(value, self.unit_var.get())

    def __repr__(self):
        return str(self.value)

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value


class VFlow(PumpCharFlow):

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
        self.value_meters = 0
        self.value_liters = 0
        self.get_both_vals(value, unit)


class PumpCharacteristic(Variable):

    def __init__(self, app, treename, dan_id, unit_ui_var):
        self.coords = {}
        self.app = app
        self.unit_var = app.builder.tkvariables.__getitem__(unit_ui_var)
        self.dan_id = dan_id
        self.tree = app.builder.get_object(treename)
        self.tkvars = app.builder.tkvariables

    def __repr__(self):
        output = 'PumpCharacteristic({}, vals:{})'.format(
            self.dan_id, self.coords)
        return output

    def load_data(self, data_dict):
        self.load_flag = True
        self.clear_characteristic()
        input_flow_vals = data_dict[self.dan_id[0]]
        input_lift_vals = data_dict[self.dan_id[1]]
        if len(input_flow_vals) == len(input_lift_vals) != 0:
            for pair in range(len(input_flow_vals)):
                self.add_point(input_flow_vals[pair], input_lift_vals[pair])
        self.sort_points()
        self.load_flag = False

    def add_point(self, flow, lift):
        """CLEAN THIS AFTER MAKING SURE OF TYPES WHICH WILL WORKS"""

        log.debug('Add point method started')
        log.debug('types: flow: {}, lift: {}'.format(type(flow), type(lift)))
        flow = round(float(flow), 3)
        lift = round(float(lift), 3)
        log.debug('types: flow: {}, lift: {}'.format(type(flow), type(lift)))
        unit = self.tkvars.__getitem__('pump_flow_unit').get()
        itemid = self.tree.insert('', tk.END, text='Punkt',
                                  values=('1', flow, lift))
        self.coords[itemid] = (PumpCharFlow(flow, unit, self.unit_var), lift)
        log.debug('char points: {}'.format(self.coords))

    def get_pump_char_func(self):
        log.debug('Getting pump characteristic func')
        pairs = {}
        flow_coords = []
        lift_coords = []
        log.debug('Starting iterating over cooridnates, {}'.format(
            self.coords))
        for point in self.coords:
            pairs[str(self.coords[point][0].value)] = self.coords[point][1]
            flow_coords.append(self.coords[point][0].value)
        log.debug(pairs)
        flow_coords.sort()
        for value in flow_coords:
            lift_coords.append(pairs[str(value)])
        log.debug('flows: {}, lifts: {}'.format(flow_coords, lift_coords))
        return flow_coords, lift_coords

    def sort_points(self):
        log.info('sort_points started')
        id_numbers = [(self.tree.set(i, 'Column_q'), i)
                      for i in self.tree.get_children('')]
        log.debug('id numbers raised: {}'.format(id_numbers))
        id_numbers.sort(key=lambda t: float(t[0]))
        for index, (val, i) in enumerate(id_numbers):
            self.tree.move(i, '', index)
            self.tree.set(i, 'Column_nr', value=str(index + 1))
        log.info('sort_points ended')

    def delete_point(self, selected_id):
        log.info('delete_point started')
        log.debug('point to delete: {}'.format(self.coords[selected_id]))
        del self.coords[selected_id]
        self.tree.delete(selected_id)
        log.debug('actual dict: {}'.format(self.coords))
        self.sort_points()
        log.info('delete_points ended')

    def clear_characteristic(self):
        id_list = []
        for id_ in self.coords:
            id_list.append(id_)
        for id_ in id_list:
            self.delete_point(id_)

    def set_unit(self, unit):
        for key in self.coords:
            self.coords[key][0].convert(unit)
            self.tree.set(key, 'Column_q', self.coords[key][0])
