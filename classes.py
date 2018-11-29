import logging
import tkinter as tk  # for python 3

import config

log = logging.getLogger('Pompa/main.classes')
unit_bracket_dict = config.unit_bracket_dict


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

    def set_trace(self, attr):
        self.ui_var.trace(
            'w', lambda *_: setattr(self, attr, self.ui_var.get())
        )

    def load_data(self, data_dict):
        if self.dan_id in data_dict:
            self.value = data_dict[self.dan_id]


class Numeric(Variable):
    """keeps rational numbers or integers and connect them with ui variables"""

    def __init__(self, app, value, ui_variable, dan_id, is_int=False):
        self.is_int = is_int
        super().__init__(app, ui_variable, dan_id)
        self.value = value
        self.set_trace('value')

    def __repr__(self):
        output = 'Numeric({}, {}, {}, {});{}'.format(
            self.app, self.value, self.dan_id, self.is_int, self.ui_var.get())
        return output

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            if not self.is_int:
                self.__dict__['value'] = float(value)
            else:
                self.__dict__['value'] = value
            if self.ui_var.get() != self.value:
                self.ui_var.set(self.value)


class Logic(Variable):
    """keeps logic variables and connect them with ui variables"""

    def __init__(self, app, value, ui_variable, dan_id, dictionary, function):
        super().__init__(app, ui_variable, dan_id)
        self.function = function
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

    def __init__(self, app, string, ui_variable, dan_id):
        super().__init__(app, ui_variable, dan_id)
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
        if self.dan_id in data_dict:
            self.string = data_dict[self.dan_id]


class Flow(Variable):
    """class for flow"""

    def __init__(self, app, value, ui_variable, dan_id, unit_ui_var,
                 unit='meters'):
        super().__init__(app, ui_variable, dan_id)
        self.unit_var = self.tkvars.__getitem__(unit_ui_var)
        self.value = value
        self.unit = unit
        self.unit_var.set(unit)
        if ui_variable in self.tkvars:
            self.set_trace('value')
        self.unit_var.trace('w', lambda *_: self.convert(self.unit_var.get()))

    def __repr__(self):
        output = 'Flow({}, {}, {}, {});{}'.format(
            self.app, self.value, self.dan_id, self.unit, self.ui_var.get())
        return output

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            self.__dict__['value'] = float(value)
            if self.__dict__['value'] != self.ui_var.get():
                self.ui_var.set(self.value)

    def convert(self, new_unit):
        log.info('conversion func starts')
        log.info('old value: {}'.format(self.value))
        if new_unit == self.unit:
            log.info('no need to conversion')
            return
        elif new_unit == 'meters':
            self.unit = new_unit
            log.debug('{} * 3.6 = {}'.format(self.value, self.value * 3.6))
            self.value = round(self.value * 3.6, 3)
        elif new_unit == 'liters':
            self.unit = new_unit
            log.debug('{} / 3.6 = {}'.format(self.value, self.value / 3.6))
            self.value = round(self.value / 3.6, 3)
        log.info('new value: {}'.format(self.value))

    def load_data(self, data_dict):
        if self.dan_id in data_dict:
            self.unit_var.set('meters')
            super().load_data(data_dict)


class PumpCharFlow(Flow):

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return str(self.value)

    def __setattr__(self, attr, value):
        self.__dict__[attr] = value


class PumpCharacteristic(Variable):

    def __init__(self, app, treename, dan_id, figure, canvas):
        self.coords = {}
        self.dan_id = dan_id
        self.figure = figure
        self.canvas = canvas
        self.tree = app.builder.get_object(treename)
        self.tkvars = app.builder.tkvariables
        self.plot = self.figure.add_subplot(111)

    def __repr__(self):
        output = 'PumpCharacteristic({}, vals:{})'.format(
            self.dan_id, self.coords)
        return output

    def load_data(self, data_dict):
        self.clear_characteristic()
        input_flow_vals = data_dict[self.dan_id[0]]
        input_lift_vals = data_dict[self.dan_id[1]]
        if len(input_flow_vals) == len(input_lift_vals) != 0:
            for pair in range(len(input_flow_vals)):
                self.add_point(input_flow_vals[pair], input_lift_vals[pair])

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
        self.coords[itemid] = (PumpCharFlow(flow, unit), lift)
        self.sort_points()
        log.debug('char points: {}'.format(self.coords))

    def draw_figure(self):
        pairs = {}
        flow_coords = []
        lift_coords = []
        self.plot.clear()
        for point in self.coords:
            pairs[str(self.coords[point][0].value)] = self.coords[point][1]
            flow_coords.append(self.coords[point][0].value)
        log.debug(pairs)
        flow_coords.sort()
        for value in flow_coords:
            lift_coords.append(pairs[str(value)])
        self.plot.plot(flow_coords, lift_coords, drawstyle='steps-pre')
        self.canvas.draw()

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
        self.draw_figure()

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
        self.draw_figure()


################################################################


class StationObject():

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.ui_vars = app.builder.tkvariables

    def __setattr__(self, attr, value):
        if '.' not in attr:
            self.__dict__[attr] = value
        else:
            attr_name, rest = attr.split('.', 1)
            setattr(getattr(self, attr_name), rest, value)

    def __getattr__(self, attr):
        if '.' not in attr:
            return self.__dict__[attr]
        else:
            attr_name, rest = attr.split('.', 1)
            return getattr(getattr(self, attr_name), rest)

    def load_data(self, data_dict):
        for attribute in self.__dict__:
            if hasattr(self.__dict__[attribute], 'dan_id'):
                self.__dict__[attribute].load_data(data_dict)


class Pipe(StationObject):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = 0
        self.parallels = 1


class Pump(StationObject):
    """class for pumps"""

    def __init__(self, app):
        super().__init__(app)
        self.cycle_time = None
        self.contour = None
        self.suction_level = None
        self.efficiency_from = None
        self.efficiency_to = None
        self.characteristic = None

    def set_flow_unit(self, unit):
        log.info('set_flow_unit started')
        unit_bracket = unit_bracket_dict[unit]
        efficiency_from_label = self.ui_vars.__getitem__(
            'pump_efficiency_from_txt')
        efficiency_to_label = self.ui_vars.__getitem__(
            'pump_efficiency_to_txt')
        add_point_label = self.ui_vars.__getitem__(
            'add_point_flow_text')
        efficiency_from_label.set('Od {}'.format(unit_bracket))
        efficiency_to_label.set('Do {}'.format(unit_bracket))
        add_point_label.set('Przepływ Q {}'.format(unit_bracket))
        log.info('self.efficiency_from type: {}'.format(
            type(self.efficiency_from)))
        self.characteristic.set_unit(unit)


class Well(StationObject):
    """class for well"""

    def __init__(self, app):
        super().__init__(app)
        self.reserve_pumps = None
        self.shape = None
        # self.set_shape(self.default['shape'])
        self.diameter = 0
        self.length = 0
        self.width = 0
        self.minimal_sewage_level = 0
        self.ord_terrain = 0
        self.ord_inlet = 0
        self.ord_outlet = 0
        self.ord_bottom = 0
        self.difference_in_start = 0
        self.ord_highest_point = 0
        self.ord_upper_level = 0
        self.inflow_max = None
        self.inflow_min = None

    def set_shape(self, shape):
        self.ui_vars.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = self.builder.get_object('Entry_Well_diameter')
        length = self.builder.get_object('Entry_Well_length')
        width = self.builder.get_object('Entry_Well_width')
        if shape == 'round':
            diameter.configure(state='normal')
            length.configure(state='disabled')
            width.configure(state='disabled')
        elif shape == 'rectangle':
            diameter.configure(state='disabled')
            length.configure(state='normal')
            width.configure(state='normal')
        log.debug('changed shape to {}'.format(shape))
