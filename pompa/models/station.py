import pompa.models.station_obj as station_object
import pompa.models.hydr_conditions as hydr_cond
import pompa.models.pipe as pipe
import pompa.models.well as well
import pompa.models.pumptype as pump_type
import pompa.models.pumpsystem as pumpsystem


class Station(station_object.StationObject):
    """
    """

    def __init__(self):
        self.well = well.Well()
        self.hydr_cond = hydr_cond.HydrConditions()
        self.ins_pipe = pipe.Pipe()
        self.out_pipe = pipe.Pipe()
        self.pump_type = pump_type.PumpType()

    def calculate(self, mode='checking'):
        self.pumpsystem = pumpsystem.PumpSystem(self, mode)
