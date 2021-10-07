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
        self.ins_pipe = pipe.Pipe()
        self.out_pipe = pipe.Pipe()
        self.out_pipes_no = v.FloatVariable(1)
        self.pump_type = pump_type.PumpType()
        self.pumpsystem = None
        # TODO: self.mode declaration

        self.variables = self._variables_map()

    def calculate(self, mode='checking'):
        """Calculates pumpsystem in a user-chosen mode"""

        self.pumpsystem = pumpsystem.PumpSystem(self, mode)

    def _variables_map(self):
        v = {}
        v['well_diameter'] = self.well.diameter
        v['well_length'] = self.well.length
        v['well_width'] = self.well.width
        v['ordinate_terrain'] = self.hydr_cond.ord_terrain
        v['ordinate_inlet'] = self.hydr_cond.ord_inlet
        v['ordinate_bottom'] = self.hydr_cond.ord_bottom
        v['ordinate_highest_point'] = self.hydr_cond.ord_highest_point
        v['ordinate_upper_level'] = self.hydr_cond.ord_upper_level
        v['ordinate_reserve_height'] = self.hydr_cond.reserve_height
        v['inflow_min'] = self.hydr_cond.inflow_min
        v['inflow_max'] = self.hydr_cond.inflow_max
        v['length_inside_pipe'] = self.ins_pipe.length
        v['diameter_inside_pipe'] = self.ins_pipe.diameter
        v['roughness_inside_pipe'] = self.ins_pipe.roughness
        v['resistance_inside_pipe'] = self.ins_pipe.resistance
        v['parallels_outside_pipe'] = self.out_pipes_no
        v['length_outside_pipe'] = self.out_pipe.length
        v['diameter_outside_pipe'] = self.out_pipe.diameter
        v['roughness_outside_pipe'] = self.out_pipe.roughness
        v['resistance_outside_pipe'] = self.out_pipe.resistance
        v['pump_contour'] = self.pump_type.contour
        v['cycle_time'] = self.pump_type.cycle_time
        v['minimal_sewage_level'] = self.pump_type.suction_level
        v['pump_efficiency_from'] = self.pump_type.efficiency_from
        v['pump_efficiency_to'] = self.pump_type.efficiency_to
        return v

