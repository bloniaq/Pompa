import pompa.models.hydr_conditions as hydr_cond
import pompa.models.pipe as pipe
import pompa.models.well as well
import pompa.models.variables as v
import pompa.models.pumptype as pump_type
import pompa.models.pumpsystem as pumpsystem
import pompa.models.figures_data as fig_data


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
        The number of parallel outside pipes
    pump_type : PumpType
        The type of pump used in station
    pumpsystem : PumpSystem
        All of pumpsets used in station

    Methods
    -------
    calculate(mode='checking')
        Calculates pumpsystem in a user-chosen mode
    """

    # noinspection PyMissingConstructor
    def __init__(self):
        # There's no need for calling super class __init__
        self.well = well.Well()
        self.hydr_cond = hydr_cond.HydrConditions()
        self.ins_pipe = pipe.Pipe("ins_pipe")
        self.out_pipe = pipe.Pipe("out_pipe")
        self.out_pipes_no = v.FloatVariable(1, name="parallel_out_pipes")
        self.mode = v.SwitchVariable('checking', name="mode")
        self.safety = v.SwitchVariable('optimal', name='safety')
        self.unit = v.SwitchVariable('m3ph', name="unit")
        self.fixing_mode = v.BoolVariable(False, name='fixing')
        self.pump_type = pump_type.PumpType()
        self.pumpsystem = None
        self.figures_data = fig_data.ChartData(self)
        self.result_data_provider = fig_data.ResultPumpsetCharData
        self.get_var = v.Variable.get_var

    def calculate(self, mode='checking'):
        """Calculates pumpsystem in a user-chosen mode"""

        self.pumpsystem = pumpsystem.PumpSystem(self, mode)

    def bind_variables(self, variables):
        for var in variables.values():
            var.modelvar = self.get_var(var.name)
            if var.modelvar is None:
                print(var.name)
                raise TypeError

    def get_figure_data(self):
        return self.figures_data.get_data()

    def min_well_dimension(self, pump_count):
        """For report purposes generates snippet with proper minimal dimensions.
        At the moment of executing this method, all calculations should be done.

        :param pump_count: int
        :return: float or tuple (of two floats)
        """
        #
        # do średnicy montażowej pompy dodano 30 cm na postawienie stopy
        # pomiędzy pompami w pompowni
        pump_d = self.pump_type.contour.get() + 0.3
        if self.well.config.get() == "singlerow":
            if self.well.shape.get() == "round":
                min_d = max(pump_count * pump_d, 1.5)
                return round(min_d, 2)
            elif self.well.shape.get() == "rectangle":
                min_l = max(pump_count * pump_d, 1.5)
                min_w = max(pump_d + 0.3, 1.5)
                return round(min_w, 2), round(min_l, 2)
        elif self.well.config.get() == "optimal":
            if self.well.shape.get() == "round":
                # https://en.wikipedia.org/wiki/Circle_packing_in_a_circle
                coeff_dict = {
                    1: 1,
                    2: 2,
                    3: 2.154,
                    4: 2.414,
                    5: 2.701,
                    6: 3,
                    7: 3,
                    8: 3.304,
                    9: 3.613,
                    10: 3.813
                }
                min_d = max(pump_d * coeff_dict[pump_count], 1.5)
                return round(min_d, 2)
            elif self.well.shape.get() == "rectangle":
                # https://en.wikipedia.org/wiki/Circle_packing_in_a_square
                coeff_dict = {
                    1: 2,
                    2: 3.414,
                    3: 3.931,
                    4: 4,
                    5: 4.828,
                    6: 5.328,
                    7: 5.732,
                    8: 5.863,
                    9: 6,
                    10: 6.747
                }
                r_d = pump_d / 2
                min_a = max(r_d * coeff_dict[pump_count], 1.5)
                return round(min_a, 2), round(min_a, 2)

    def check_well_area_for_pumps(self, pumps_count):

        pump_c = self.pump_type.contour.value
        safe_pump_c = self.pump_type.contour.value + 0.3

        def rectangle_singlerow():
            # No unused area around pump : contour = pump_c
            side = max(self.well.length.value, self.well.width.value)
            pumps_len = pumps_count * pump_c
            return pumps_len <= side

        def rectangle_optimal():
            # Installation area around pump : contour = safe_pump_c
            wi = self.well.width.value
            le = self.well.length.value
            safe_radius = safe_pump_c / 2

            def dim_setup(a, b):

                # a >= (2m + 1) * r
                # after reformulation:
                rows = ((a/safe_radius) - 1) // 2
                # b >= (2 + (n - 1)sqrt(3)) * r
                # after reformulation:
                columns = (((b/safe_radius) - 2) // (3 ** (1/2))) + 1

                return rows * columns

            return max(dim_setup(wi, le), dim_setup(le, wi)) >= pumps_count

        def round_singlerow():
            # No unused area around pump : contour = pump_c
            # min_d = 1,5 # meters
            diameter = self.well.diameter.value
            pumps_len = pumps_count * pump_c
            min_d = max(pumps_len, 1.5)
            return min_d <= diameter

        def round_optimal():
            # Installation area around pump : contour = safe_pump_c
            # min_d = 1,5 # meters

            coeff_dict = {
                1: 1,
                2: 2,
                3: 2.154,
                4: 2.414,
                5: 2.701,
                6: 3,
                7: 3,
                8: 3.304,
                9: 3.613,
                10: 3.813
            }

            min_d = max(safe_pump_c * coeff_dict[pumps_count], 1.5)
            return self.well.diameter.value >= min_d

        result = {
            'rectangle': {'singlerow': rectangle_singlerow,
                          'optimal': rectangle_optimal},
            'round': {'singlerow': round_singlerow,
                      'optimal': round_optimal}
        }

        return result[self.well.shape.get()][self.well.config.get()]()

    def validate_dead_volume_under_inlet(self):
        dead_vol_ord = self.hydr_cond.ord_bottom.value + \
                       self.pump_type.suction_level.value
        print('dead vol ord', dead_vol_ord)
        print('reserve_height', self.hydr_cond.reserve_height.value)
        print('hydr_cond.ord_inlet', self.hydr_cond.ord_inlet.value)
        return dead_vol_ord + self.hydr_cond.reserve_height.value <=\
            self.hydr_cond.ord_inlet.value

    def validate_min_ins_pipe_length(self):
        ord_lowest = self.hydr_cond.ord_bottom.value + \
                     self.pump_type.suction_level.value
        min_ins_pipe_len = self.hydr_cond.ord_outlet.value - ord_lowest + 1
        return self.ins_pipe.length >= min_ins_pipe_len
