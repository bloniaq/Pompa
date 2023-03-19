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
        self.cycle_time = v.IntVariable(name="min_cycle_time")
        self.contour = v.FloatVariable(name="pump_contour")
        self.suction_level = v.FloatVariable(name="suction_level")
        self.efficiency_from = v.FlowVariable(name="pump_eff_min")
        self.efficiency_to = v.FlowVariable(name="pump_eff_max")
        self.characteristic = v.PumpCharVariable(name="pump_characteristic")

    def opt_range(self, pumps_amount):
        """Return pumpset efficiency optimal range

        Parameters
        ----------
        pumps_amount : int
            The number of pumps
        """
        range_start_value = self.efficiency_from.value_m3ph * pumps_amount
        """
        Te zakomentowane linijki to stare rozwiazanie, które powodowało że 
        próba wykonania powtórnych obliczeń była blokowana z powodu powołania
        zmienny o zajętej już nazwie. Problem unikalności zmiennych w modelu
        należałoby jakoś w przyszłości rozwiązać
        """
        # range_start = v.FlowVariable(range_start_value, "m3ph",
        #                              f"opt_ran_start_pump_{pumps_amount}")
        range_start = v.FlowVariable(range_start_value, "m3ph", name=None)
        range_stop_value = self.efficiency_to.value_m3ph * pumps_amount
        # range_stop = v.FlowVariable(range_stop_value, "m3ph",
        #                             f"opt_ran_stop_pump_{pumps_amount}")
        range_stop = v.FlowVariable(range_stop_value, "m3ph", None)
        return range_start, range_stop

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

        shutdown_ordinate = v.FloatVariable(
            self.suction_level.value + ord_bottom.value)

        return shutdown_ordinate
