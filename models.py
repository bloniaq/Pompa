class Flow():
    """class for flow"""

    def __init__(self, flow_val, flow_unit):
        self.value = flow_val
        self.unit = flow_unit

    def convert(self, new_unit):
        pass


class Lift():
    """class for lift"""

    def __init__(self, lift_val, lift_unit):
        self.value = lift_val
        self.unit = lift_unit

    def convert(self, new_unit):
        pass


class Pipe():
    """class for pipes"""

    def __init__(self):
        self.length = 0
        self.dimension = 0
        self.grittiness = 0
        self.local_resitance = []
        self.parallels = 1

    def value_to_cvar(self, app, variable):
        var = app.builder.get_variable(variable)
        




class Pump():
    """class for pumps"""

    def __init__(self):
        self.cycle_time = 0
        self.contour = 0
        self.characteristic = {}
        self.efficiency = []
        self.suction_level = 0

    def add_characteristic_points(
            self, point_id, flow_val, flow_unit, lift_val, lift_unit):
        flow = Flow(flow_val, flow_unit)
        lift = Lift(lift_val, lift_unit)
        self.characteristic[point_id] = (flow, lift)
        self.sort_characteristic_points()

    def sort_characteristic_points(self):
        pass


class Well():
    """class for well"""

    dan_shape = {'0': 'rectangle', '1': 'round'}
    dan_configuration = {'0': 'linear', '1': 'optimal'}
    dan_reserve = {'1': 'minimal', '2': 'optimal', '3': 'safe'}

    def __init__(self):
        self.configuration = 'round'
        self.reserve_pumps = 'safe'
        self.shape = 'round'
        self.dimension = 0
        self.length = 0
        self.width = 0
        self.ord_terrain = 0
        self.ord_inlet = 0
        self.ord_outlet = 0
        self.ord_bottom = 0
        self.ord_start = 0
        self.ord_highest_point = 0
        self.ord_upper_level = 0
        self.influx_max = 0
        self.influx_min = 0

    def set_shape(self, new_shape):
        self.shape = new_shape
        if self.shape == 'round':
            pass
        elif self.shape == 'rectangle':
            pass
