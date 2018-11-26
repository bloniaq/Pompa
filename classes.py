import logging
import tkinter as tk  # for python 3

import config

log = logging.getLogger('Pompa/main.classes')
unit_bracket_dict = config.unit_bracket_dict


class Variable():

    def __init__(self, app):
        self.app = app
        self.builder = app.builder
        self.variables = {}

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

    def set_var_value(self, variable_name, value):
        log.info('setting {} value to: {}'.format(variable_name, value))
        attribute = self.variables[variable_name][0]
        setattr(self, attribute, value)
        try:
            variable = self.builder.get_variable(variable_name)
        except KeyError as e:
            log.warning('variable <{}> doesn\'t exist'.format(e))
        else:
            if variable.get() != value:
                variable.set(value)
            log.debug('{} - var value: {}, ui var value: {}'.format(
                variable_name, getattr(self, attribute), variable.get()))

    def bind_traceing_to_ui_variables(self):
        for variable in self.variables:
            if variable in self.app.builder.tkvariables:
                log.debug('variable: {}'.format(variable))
                variable_object = self.builder.get_variable(variable)
                variable_object.trace(
                    'w', lambda *_,
                    var=variable: self.app.set_var_value(var, self)
                )

    def load_data(self, data_dict):
        for variable in self.variables:
            if self.variables[variable][1] in data_dict:
                self.set_var_value(
                    variable, data_dict[self.variables[variable][1]])

    '''
    def load_data(self, data_dict):
        for variable in self.variables:
            if (variable in self.app.builder.tkvariables and
                    self.variables[variable][1] in data_dict):
                self.set_var_value(
                    variable, data_dict[self.variables[variable][1]])
    '''


class Flow():
    """class for flow"""

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return str(self.value)

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


class Resistance():
    """class for lift"""

    def __init__(self):
        self.string = ''
        self.values = []

    def __setattr__(self, attribute, value):
        if attribute != 'string':
            super().__setattr__(attribute, value)
        elif value != '':
            super().__setattr__(attribute, value)
            self.values = [float(s) for s in value.split(',')]


class Pipe(Variable):
    """class for pipes"""

    def __init__(self, app):
        super().__init__(app)
        self.length = 0
        self.diameter = 0
        self.roughness = 0
        self.resistance = Resistance()
        self.parallels = 1


class Pump(Variable):
    """class for pumps"""

    def __init__(self, app):
        super().__init__(app)
        self.tree = self.builder.get_object('Treeview_Pump')
        self.cycle_time = 0
        self.contour = 0
        self.characteristic = {}
        self.suction_level = 0
        self.pump_flow_coords = []
        self.pump_lift_coords = []
        self.efficiency_from = Flow(
            0, self.builder.tkvariables.__getitem__('pump_flow_unit').get())
        self.efficiency_to = Flow(
            0, self.builder.tkvariables.__getitem__('pump_flow_unit').get())
        self.set_flow_unit(
            self.builder.tkvariables.__getitem__('pump_flow_unit').get())

    def add_point(self, flow, lift):
        log.debug('Add point method started')
        log.debug('types: flow: {}, lift: {}'.format(type(flow), type(lift)))
        flow = round(float(flow), 3)
        lift = round(float(lift), 3)
        log.debug('types: flow: {}, lift: {}'.format(type(flow), type(lift)))
        unit = self.builder.tkvariables.__getitem__('pump_flow_unit').get()
        itemid = self.tree.insert('', tk.END, text='Punkt',
                                  values=('1', flow, lift))
        self.characteristic[itemid] = (Flow(flow, unit), lift)
        self.sort_points()
        log.debug('char points: {}'.format(self.characteristic))

    def load_characteristic_coords(self):
        if len(self.pump_flow_coords) == len(self.pump_lift_coords) != 0:
            for coord in range(len(self.pump_flow_coords)):
                self.add_point(self.pump_flow_coords[coord],
                               self.pump_lift_coords[coord])

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
        log.debug('point to delete: {}'.format(
            self.characteristic[selected_id]))
        del self.characteristic[selected_id]
        self.tree.delete(selected_id)
        log.debug('actual dict: {}'.format(self.characteristic))
        self.sort_points()
        log.info('delete_points ended')

    def set_flow_unit(self, unit):
        log.info('set_flow_unit started')
        unit_bracket = unit_bracket_dict[unit]
        efficiency_from_label = self.builder.tkvariables.__getitem__(
            'pump_efficiency_from_txt')
        efficiency_to_label = self.builder.tkvariables.__getitem__(
            'pump_efficiency_to_txt')
        add_point_label = self.builder.tkvariables.__getitem__(
            'add_point_flow_text')
        efficiency_from_label.set('Od {}'.format(unit_bracket))
        efficiency_to_label.set('Do {}'.format(unit_bracket))
        add_point_label.set('Przepływ Q {}'.format(unit_bracket))
        log.info('self.efficiency_from type: {}'.format(
            type(self.efficiency_from)))
        self.efficiency_from.convert(unit)
        self.builder.tkvariables.__getitem__('pump_efficiency_from').set(
            self.efficiency_from.value)
        self.efficiency_to.convert(unit)
        self.builder.tkvariables.__getitem__('pump_efficiency_to').set(
            self.efficiency_to.value)
        for key in self.characteristic:
            self.characteristic[key][0].convert(unit)
            self.tree.set(key, 'Column_q', self.characteristic[key][0])


class Well(Variable):
    """class for well"""

    default = config.default

    def __init__(self, app):
        super().__init__(app)
        self.reserve_pumps = 'safe'
        self.shape = self.builder.tkvariables.__getitem__('shape')
        self.set_shape(self.default['shape'])
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
        self.inflow_max = Flow(0, 'liters')
        self.inflow_min = Flow(0, 'liters')
        # self.bind_traces_manual(self.app)

    def set_shape(self, shape):
        self.builder.tkvariables.__getitem__('shape').set(shape)
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

    def bind_traces_manual(self, app):
        variable = 'inflow_max'
        log.debug('variable: {}'.format(variable))
        variable_object = self.builder.get_variable(variable)
        variable_object.trace(
            'w', lambda *_,
            var=variable: app.set_var_value(var, self.inflow_max)
        )
