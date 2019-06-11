# libraries
import logging

# modules
import models.models as models

log = logging.getLogger('pompa.station')


class Station(models.StationObject):

    def __init__(self, app):
        super().__init__(app)

        # components
        self.well = None
        self.ins_pipe = None
        self.out_pipe = None
        self.pump = None

        # input parameters
        self.minimal_sewage_level = None
        self.ord_terrain = None
        self.ord_inlet = None
        self.ord_outlet = None
        self.ord_bottom = None
        self.difference_in_start = None
        self.ord_highest_point = None
        self.ord_upper_level = None
        self.inflow_max = None
        self.inflow_min = None

        # parameters to update
        self.min_sew_ord = None

    def update(self):
        self.well.update()
        self.pump.update()
        self.ins_pipe.update()
        self.out_pipe.update()
        self.min_sew_ord = self.minimal_sewage_level()

    def height_to_pump(self, lower_ord):
        height = self.ord_upper_level.value - lower_ord
        return height

    def minimal_sewage_level(self):
        return self.ord_bottom.value + self.minimal_sewage_level.value

    def pipes_ready(self):
        """returns if there both pipe has data to draw figures
        """
        log.debug('Are pipes ready?')
        flag = True
        if not self.ins_pipe.pipe_char_ready():
            flag = False
        log.debug(flag)
        if not self.out_pipe.pipe_char_ready():
            flag = False
        log.debug(flag)
        return flag

    def geom_loss_ready(self):
        log.debug('Are pipes ready?')
        flag = True
        checklist = [self.ord_bottom, self.minimal_sewage_level]
        for parameter in checklist:
            if parameter is None:
                flag = False
                return flag
        for parameter in checklist:
            log.debug('{} = {}'.format(parameter, parameter.value))
            if parameter.value == 0:
                flag = False
        return flag

    def pump_set_ready(self):
        flag = True
        if self.pump_set is None:
            flag = False
        if self.number_of_pumps == 1:
            flag = False
        return flag

    def velocity(self, height):
        velocity = self.well.cross_sectional_area() * height
        log.debug('v for h: {} is {}'.format(height, velocity))
        return velocity

    def get_calculative_flow(self):
        return self.inflow_max.value_liters * 1.4
