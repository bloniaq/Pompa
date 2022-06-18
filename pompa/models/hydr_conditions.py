import pompa.models.variables as v


class HydrConditions:
    """Class used to keep hydraulic conditions of sewage pumping station

    Attributes
    ----------
    ord_terrain : FloatVariable
        The ordinate of terrain near sewage pumping station.
    ord_inlet : FloatVariable
        The ordinate of lowest inlet pipe.
    ord_outlet : FloatVariable
        The ordinate of outlet pipe.
    ord_bottom : FloatVariable
        Assumed ordinate of bottom of well.
    ord_highest_point : FloatVariable
        The highest point on pipe rout ordinate.
    ord_upper_level : FloatVariable
        The ordinate of end of outside pipe(s).
    reserve_height : FloatVariable
        Assumed distance between inlet ordinate and alarm ordinate.
    inflow_max : FlowVariable
        Assumed maximum inflow to sewage pumping station.
    inflow_min : FlowVariable
        Assumed minimum inflow to sewage pumping station.

    Methods
    -------
    geom_height(ordinate)
        Returns difference between upper level ordinate and parameter ordinate.
    """

    def __init__(self):
        self.ord_terrain = v.FloatVariable(name='ord_terrain')
        self.ord_inlet = v.FloatVariable(name='ord_inlet')
        self.ord_outlet = v.FloatVariable(name='ord_outlet')
        self.ord_bottom = v.FloatVariable(name='ord_bottom')
        self.ord_highest_point = v.FloatVariable(name='ord_highest_point')
        self.ord_upper_level = v.FloatVariable(name='ord_upper_level')
        self.reserve_height = v.FloatVariable(name='reserve_height')
        self.inflow_max = v.FlowVariable(name='inflow_max')
        self.inflow_min = v.FlowVariable(name='inflow_min')

    def geom_height(self, ordinate):
        """Return geometric height to pump

        Parameters
        ----------
        ordinate : FloatVariable
            Ordinate to check.

        Returns
        -------
        FloatVariable
            Difference between checked ordinate and upper level ordinate
        """

        height = self.ord_upper_level.value - ordinate.value
        return v.FloatVariable(height, name="geom_height")
