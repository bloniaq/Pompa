import pompa.models.variables as v


class PumpType(v.StationObject):
    """Class used to keep type of pump used in Sewage Pumping Station

    Attributes
    ----------
    cycle_time : IntVariable
        Minimal cycle time declared by pump manufacturer
    contour : FloatVariable
        Minimal radius needed to pump installation
    suction_level : FloatVariable
        Minimal level of sewage which can't be pumped by pump
    efficiency_from : FlowVariable
        Minimum value of best pump efficiency range
    efficiency_to : FlowVariable
        Maximum value of best pump efficiency range
    characteristic : PumpCharVariable
        Set of pump characteristic graph points
    """

    def __init__(self):
        self.cycle_time = v.IntVariable()
        self.contour = v.FloatVariable()
        self.suction_level = v.FloatVariable()
        self.efficiency_from = v.FlowVariable()
        self.efficiency_to = v.FlowVariable()
        self.characteristic = v.PumpCharVariable()
