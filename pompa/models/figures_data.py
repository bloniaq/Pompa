import numpy as np


class ChartData:

    def __init__(self, station):
        self.station = station
        self.hydr_cond = station.hydr_cond
        self.ins_pipe = station.ins_pipe
        self.out_pipe = station.out_pipe
        self.pump = station.pump_type

        self.pipe_chart = PipeChartData(self.hydr_cond, self.ins_pipe,
                                        self.out_pipe)
        self.pump_chart = PumpCharData()

        self.pointer = {
            'pipechart_data': self.pipe_chart,
            'pumpchart_data': self.pump_chart
        }

    def get_data(self):
        data = {
            'pipechart_data': 'Not enough data',
            'pumpchart_data': 'Not enough data'
        }
        for chart in data.keys():
            data[chart] = self.pointer[chart].get_data()
        return data


class PipeChartData:

    def __init__(self, hydr_cond, ins_pipe, out_pipe):
        self.hydr_cond = hydr_cond
        self.ins_pipe = ins_pipe
        self.out_pipe = out_pipe

    def get_data(self):

        empty_data = {
            'x': None,
            'y_ins_pipe': None,
            'y_geom_h': None,
            'y_out_pipe': None,
            'y_coop': None
        }

        if not self.check_conditions():
            return empty_data
        else:
            return self.prepare_data()

    def prepare_data(self):

        ins_pipe_poly_coeffs = self.ins_pipe.dynamic_loss_polynomial(
            self.hydr_cond.inflow_min,
            self.hydr_cond.inflow_max
        )
        out_pipe_poly_coeffs = self.out_pipe.dynamic_loss_polynomial(
            self.hydr_cond.inflow_min,
            self.hydr_cond.inflow_max
        )
        # print("ins pipe polynomial:")
        # print(np.poly1d(ins_pipe_poly_coeffs))
        # print("out pipe polynomial:")
        # print(np.poly1d(out_pipe_poly_coeffs))

        geom_height = self.hydr_cond.geom_height(self.hydr_cond.ord_outlet)

        data = {
            'x': self.create_x_array(),
            'y_ins_pipe': np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs) + geom_height,
            'y_geom_h': np.polynomial.polynomial.Polynomial(
                geom_height),
            'y_out_pipe': np.polynomial.polynomial.Polynomial(
                out_pipe_poly_coeffs) + geom_height,
            'y_coop': np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs) + np.polynomial.polynomial.Polynomial(
                out_pipe_poly_coeffs) + geom_height
        }

        return data

    def create_x_array(self):
        array = np.linspace(
            0.9 * self.hydr_cond.inflow_min.get_by_unit('m3ps'),
            1.6 * self.hydr_cond.inflow_max.get_by_unit('m3ps'),
            10
        )
        return array

    def check_conditions(self):
        if not self.figure_preconditions():
            return False
        availability = self.available_figures()
        if not any(availability.values()):
            return False
        return True

    def available_figures(self):
        result = {
            'geometric_height': self.geom_h_figure_ready(),
            'ins_pipe': self.ins_pipe_figure_ready(),
            'out_pipe': self.out_pipe_figure_ready(),
            'cooperation': all([self.ins_pipe_figure_ready(),
                                self.out_pipe_figure_ready()])
        }

        return result

    def figure_preconditions(self):
        rules = [
            self.hydr_cond.inflow_max.value_lps > 0,
            self.hydr_cond.inflow_min.value_lps > 0,
            self.hydr_cond.inflow_max.value_lps > self.hydr_cond.inflow_min.value_lps
        ]
        return all(rules)

    def geom_h_figure_ready(self):
        rules = [
            self.hydr_cond.ord_upper_level.value <= self.hydr_cond.ord_highest_point.value,
            self.hydr_cond.ord_outlet < self.hydr_cond.ord_highest_point
        ]
        return all(rules)

    def ins_pipe_figure_ready(self):
        rules = [
            self.ins_pipe.length.value > 0,
            self.ins_pipe.diameter.value > 0,
            self.ins_pipe.roughness.value > 0,
        ]
        return all(rules)

    def out_pipe_figure_ready(self):
        rules = [
            self.out_pipe.length.value > 0,
            self.out_pipe.diameter.value > 0,
            self.out_pipe.roughness.value > 0,
        ]
        return all(rules)


class PumpCharData:

    def __init__(self):
        pass

    def get_data(self):
        return None

    def check_conditions(self):
        return None