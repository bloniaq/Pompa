import numpy as np


class ChartData:

    def __init__(self, station):
        self.station = station
        self.hydr_cond = station.hydr_cond
        self.ins_pipe = station.ins_pipe
        self.out_pipe = station.out_pipe
        self.pump = station.pump_type

        self.pipe_chart = PipeChartData(self.hydr_cond,
                                        self.ins_pipe,
                                        self.out_pipe)

    def get_data(self):
        data = {
            'pipechart_data': 'Not enough data',
            'pumpchart_data': 'Not enough data'
        }
        if not self.check_conditions():
            return data
        data['pipechart_data'] = self.pipe_chart.prepare_data()
        return data

    def check_conditions(self):
        if not self.station.figure_preconditions():
            return False
        availability = self.station.available_figures()
        if not any(availability.values()):
            return False
        return True

class PipeChartData:

    def __init__(self, hydr_cond, ins_pipe, out_pipe):
        self.hydr_cond = hydr_cond
        self.ins_pipe = ins_pipe
        self.out_pipe = out_pipe

    def prepare_data(self):

        def flows_array(unit):
            array = np.linspace(
                self.hydr_cond.inflow_min.get_by_unit(unit),
                1.4 * self.hydr_cond.inflow_max.get_by_unit(unit),
                10
            )
            return array

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
            'x': flows_array('m3ps'),
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