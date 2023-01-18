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
        self.pump_chart = PumpCharData(self.hydr_cond, self.pump)

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

        checked_data = self.check_conditions(empty_data)

        if not checked_data['x']:
            return checked_data

        return self.prepare_data(checked_data)

    def prepare_data(self, data_container):

        if data_container['x']:
            data_container['x'] = self.create_x_array()
        if data_container['y_geom_h']:
            geom_height = self.hydr_cond.geom_height(self.hydr_cond.ord_outlet)
        else:
            geom_height = 0
        data_container['y_geom_h'] = np.polynomial.polynomial.Polynomial(geom_height)
        if data_container['y_ins_pipe']:
            ins_pipe_poly_coeffs = self.ins_pipe.dynamic_loss_polynomial(
                self.hydr_cond.inflow_min,
                self.hydr_cond.inflow_max
            )
            data_container['y_ins_pipe'] = np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs) + geom_height
        if data_container['y_out_pipe']:
            out_pipe_poly_coeffs = self.out_pipe.dynamic_loss_polynomial(
                self.hydr_cond.inflow_min,
                self.hydr_cond.inflow_max
            )
            data_container['y_out_pipe'] = np.polynomial.polynomial.Polynomial(
                out_pipe_poly_coeffs) + geom_height
            print('outputed data container for out pipe: ', data_container['y_out_pipe'])
        if data_container['y_coop'] and data_container['y_out_pipe'] and data_container['y_ins_pipe']:
            data_container['y_coop'] = np.polynomial.polynomial.Polynomial(
                ins_pipe_poly_coeffs) + np.polynomial.polynomial.Polynomial(
                out_pipe_poly_coeffs) + geom_height

        return data_container

    def create_x_array(self):
        array = np.linspace(
            0.9 * self.hydr_cond.inflow_min.get_by_unit('m3ps'),
            1.6 * self.hydr_cond.inflow_max.get_by_unit('m3ps'),
            10
        )
        return array

    def check_conditions(self, container):
        if not self.figure_preconditions():
            return container

        validators = {
            'x': self.figure_preconditions(),
            'y_geom_h': self.geom_h_figure_ready(),
            'y_ins_pipe': self.ins_pipe_figure_ready(),
            'y_out_pipe': self.out_pipe_figure_ready(),
            'y_coop': all([self.ins_pipe_figure_ready(),
                                self.out_pipe_figure_ready()])
        }
        for figure in validators.keys():
            container[figure] = validators[figure]
        return container

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

    def __init__(self, hydr_cond, pumptype):
        self.hydr_cond = hydr_cond
        self.pumptype = pumptype

    def get_data(self):
        empty_data = {
            'x': None,
            'y_p_char': None,
            'y_p_eff': None,
        }
        if not self.check_conditions():
            return empty_data
        else:
            return self.prepare_data()

    def check_conditions(self):
        return False

    def prepare_data(self):
        pump_polynomial = self.pumptype.characteristic.polynomial_coeff()
        data = {
            'x': self.create_x_array(),
            'y_p_char': pump_polynomial,
            'y_p_eff': None
        }
        return data

    def create_x_array(self):
        start = min(self.hydr_cond.inflow_min, self.pumptype.efficiency_from)
        stop = max(self.hydr_cond.inflow_max, self.pumptype.efficiency_to)
        array = np.linspace(
            0.9 * start.get_by_unit('m3ps'),
            1.6 * stop.get_by_unit('m3ps'),
            10
        )
        return array