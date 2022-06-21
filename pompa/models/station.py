import pompa.models.hydr_conditions as hydr_cond
import pompa.models.pipe as pipe
import pompa.models.well as well
import pompa.models.variables as v
import pompa.models.pumptype as pump_type
import pompa.models.pumpsystem as pumpsystem


class Station(v.StationObject):
    """Class used to keep the Sewage Pumping Station

    Attributes
    ----------
    well : Well
        The well of station
    hydr_cond : HydrConditions
        The hydraulic conditions of station
    ins_pipe : Pipe
        The pipe(s) inside station
    out_pipe : Pipe
        The pipe(s) outside station
    out_pipes_no : FloatVariable
        The number of parallel outisde pipes
    pump_type : PumpType
        The type of pump used in station
    pumpsystem : PumpSystem
        All of pumpsets used in station

    Methods
    -------
    calculate(mode='checking')
        Calculates pumpsystem in a user-chosen mode
    """

    def __init__(self):
        self.well = well.Well()
        self.hydr_cond = hydr_cond.HydrConditions()
        self.ins_pipe = pipe.Pipe("ins_pipe")
        self.out_pipe = pipe.Pipe("out_pipe")
        self.out_pipes_no = v.FloatVariable(1, name="parallel_out_pipes")
        self.mode = v.SwitchVariable('checking', name="mode")
        self.safety = v.SwitchVariable('optimal', name='safety')
        self.unit = v.SwitchVariable('meters', name="unit")
        self.pump_type = pump_type.PumpType()
        self.pumpsystem = None
        self.get_var = v.Variable.get_var

    def calculate(self, mode='checking'):
        """Calculates pumpsystem in a user-chosen mode"""

        self.pumpsystem = pumpsystem.PumpSystem(self, mode)

    def bind_variables(self, variables):
        for var in variables:
            var.modelvar = self.get_var(var.name)
