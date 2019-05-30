import logging
import tkinter as tk  # for python 3

log = logging.getLogger('Pompa.variables')


class Variable():

    load_flag = False

    def __init__(self, app, ui_variable, data_id, fig_depend):
        self.fig_depend = fig_depend
        self.app = app
        self.builder = app.builder
        # self.tkvars = app.builder.tkvariables
        # deleted alias
        self.data_id = data_id
        if ui_variable in self.builder.tkvariables:
            self.ui_var = self.builder.tkvariables.__getitem__(ui_variable)
        else:
            log.error('No ui_variable named {}'.format(ui_variable))
            self.ui_var = None

    def set_trace(self, attr):
        self.ui_var.trace('w', lambda *_: self.update_attribute(attr))

    def update_attribute(self, attr):
        """ Returns nothing

        Sets value of ui var to attribute value.
        Refreshes charts if flag say so.
        """
        ui_content = self.ui_var.get()
        setattr(self, attr, ui_content)

        if self.fig_depend and not self.load_flag:
            self.app.update_fig_calculations()
            self.app.prepare_figure(self.fig_depend)
            # TODO:
            # write those functions

    def load_data(self, data_dict):
        self.load_flag = True
        if self.dan_id in data_dict:
            self.value = data_dict[self.dan_id]
        self.load_flag = False


class P_Int(Variable, int):

    def __new__(cls, app, value, ui_variable, data_id, fig_depend=False):
        return int.__new__(cls, value)

    def __init__(self, app, value, ui_variable, data_id, fig_depend=False):
        Variable.__init__(app, ui_variable, data_id, fig_depend)

    def __setattr__(self, attr, value):
        if attr != 'value':
            self.__dict__[attr] = value
        else:
            self.__dict__['value'] = value
            self.ui_var.set(self.value)
            if self.fig_depend and not self.load_flag:
                try:
                    self.app.draw_auxillary_figures()
                except (AttributeError, TypeError) as e:
                    log.error('Error {}'.format(e))
