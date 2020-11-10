import pompa.models.variables as v


class HydrConditions():
    """
    """

    def __init__(self):
        self.ord_terrain = v.FloatVariable()
        self.ord_inlet = v.FloatVariable()
        self.ord_outlet = v.FloatVariable()
        self.ord_bottom = v.FloatVariable()
        self.ord_highest_point = v.FloatVariable()
        self.ord_upper_level = v.FloatVariable()
        self.inflow_max = v.FlowVariable()
        self.inflow_min = v.FlowVariable()
