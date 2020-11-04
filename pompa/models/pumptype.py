import models.station_obj as station_object
import models.variables as v


class Pump_Type(station_object.StationObject):

    def __init__(self):
        self.cycle_time = v.IntVariable()
        self.contour = v.FloatVariable()
        self.suction_level = v.FloatVariable()
        self.efficiency_from = v.FlowVariable()
        self.efficiency_to = v.FlowVariable()
        self.characteristic = v.PumpCharVariable()

    def max_efficiency(self):
        avg = ((self.efficiency_from.value_m3ph
               + self.efficiency_to.value_m3ph)
               / 2)
        return v.FlowVariable(avg)