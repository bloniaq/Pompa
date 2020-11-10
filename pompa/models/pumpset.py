class PumpSet():

    def __init__(self, pump_type, stop_ord, w_pump_amount, inflow_min,
                 inflow_max):
        self.pump_type = pump_type
        self.stop_ord = stop_ord
        self.w_pump_amount = w_pump_amount
        self.inflow_min = inflow_min
        self.inflow_max = inflow_max
