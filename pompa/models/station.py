import models.station_obj as station_object
import models.hydr_conditions as hydr_cond
import models.pipe as pipe
import models.well as well
import models.pumptype as pump_type


class Station(station_object.StationObject):
    """
    """

    def __init__(self):
        self.well = well.Well()
        self.hydr_cond = hydr_cond.HydrConditions()
        self.ins_pipe = pipe.Pipe()
        self.out_pipe = pipe.Pipe()
        self.pump_type = pump_type.Pump_Type()
