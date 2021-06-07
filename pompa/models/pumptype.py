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

    Methods
    -------
    opt_range(pumps_amount)
        Returns optimal range of pumpset efficiency.
    shutdown_ord(ord_bottom)
        Returns pumpset shutdown ordinate.
    """

    def __init__(self):
        self.cycle_time = v.IntVariable()
        self.contour = v.FloatVariable()
        self.suction_level = v.FloatVariable()
        self.efficiency_from = v.FlowVariable()
        self.efficiency_to = v.FlowVariable()
        self.characteristic = v.PumpCharVariable()

    def opt_range(self, pumps_amount):
        """Return pumpset efficiency optimal range

        Parameters
        ----------
        pumps_amount : int
            The number of pumps
        """
        return self.efficiency_from * pumps_amount, self.efficiency_to * 2

    def shutdown_ord(self, ord_bottom):
        """Calculate ordinate of pump shutdown.

        Parameters
        ----------
        ord_bottom : FloatVariable
            Current station bottom ordinate

        Returns
        -------
        FloatVariable
            Sum of current bottom ordinate and pumptype suction level.
        """

        return self.suction_level + ord_bottom

