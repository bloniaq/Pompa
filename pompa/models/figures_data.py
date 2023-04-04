import numpy as np


class ChartData:

    def __init__(self, station):
        self.station = station
        self.hydr_cond = station.hydr_cond
        self.ins_pipe = station.ins_pipe
        self.out_pipe = station.out_pipe
        self.pump = station.pump_type

        self.pipe_chart = PipeChartData(self.hydr_cond, self.ins_pipe,
                                        self.out_pipe, self.pump.shutdown_ord)
        self.pump_chart = PumpCharData(self.hydr_cond, self.pump, station.fixing_mode)

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

    def __init__(self, hydr_cond, ins_pipe, out_pipe, get_shutdown_ord):
        self.hydr_cond = hydr_cond
        self.ins_pipe = ins_pipe
        self.out_pipe = out_pipe
        self.get_shutdown_ord = get_shutdown_ord

    def get_data(self):
        empty_data = {
            'x': None,
            'y_ins_pipe': None,
            'y_geom_h': None,
            'y_out_pipe': None,
            'y_coop': None
        }
        checked_data = self.check_conditions(empty_data)
        return self.prepare_data(checked_data)

    def prepare_data(self, data_container):

        if data_container['x']:
            data_container['x'] = self.create_x_array()
        else:
            return data_container
        if data_container['y_geom_h']:
            shutdown_ord = self.get_shutdown_ord(self.hydr_cond.ord_bottom)
            geom_height = self.hydr_cond.geom_height(shutdown_ord)
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
        if not self._figure_preconditions():
            return container

        validators = {
            'x': self._figure_preconditions(),
            'y_geom_h': self.geom_h_figure_ready(),
            'y_ins_pipe': self.ins_pipe_figure_ready(),
            'y_out_pipe': self.out_pipe_figure_ready(),
            'y_coop': all([self.ins_pipe_figure_ready(),
                                self.out_pipe_figure_ready()])
        }
        for figure in validators.keys():
            container[figure] = validators[figure]
        return container

    def _figure_preconditions(self):
        rules = [
            self.hydr_cond.inflow_max.value_lps > 0,
            self.hydr_cond.inflow_min.value_lps > 0,
            self.hydr_cond.inflow_max.value_lps > self.hydr_cond.inflow_min.value_lps
        ]
        return all(rules)

    def geom_h_figure_ready(self):
        rules = [
            self.hydr_cond.ord_outlet < self.hydr_cond.ord_upper_level
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

    def __init__(self, hydr_cond, pumptype, fixing_mode):
        self.hydr_cond = hydr_cond
        self.pumptype = pumptype
        self.fixing_mode = fixing_mode

    def get_data(self):
        """
        Every key-value pair has to have proper comparision procedure for
        checking if data for chart has changed. Adding pair has to be followed
        in making that procedure there.
        """
        data = {
            'x': None,
            'y_p_points': None,
            'y_p_char': None,
            'y_p_eff': None,
        }
        # return empty dictionary if conditions for graph are unfulfilled
        if not self._figure_preconditions():
            return data
        else:
            data['x'] = self._create_x_array()
            data['y_p_points'] = self._prepare_points()
        if self._pump_char_ready():
            polynomial = self._prepare_polynomial()
            data['y_p_char'] = polynomial
            data['y_p_eff'] = self._create_efficiency_data(polynomial)
        return data

    def _prepare_points(self):
        x_coords = [p[0].value_m3ps for p in self.pumptype.characteristic.value]
        y_coords = [p[1] for p in self.pumptype.characteristic.value]
        return (x_coords, y_coords)

    def _prepare_polynomial(self):
        polyfit = self.pumptype.characteristic.polynomial_coeff(
            fixing_mode=self.fixing_mode)
        pump_polynomial = np.polynomial.Polynomial(polyfit)
        return pump_polynomial

    def _create_x_array(self):
        p_flows = [f[0] for f in self.pumptype.characteristic.value]
        start = min(p_flows[0], self.pumptype.efficiency_from)
        stop = max(p_flows[-1].value_m3ps,
                   1.6 * self.pumptype.efficiency_to.value_m3ps)
        array = np.linspace(
            0.9 * start.get_by_unit('m3ps'),
            stop,
            10
        )
        return array

    def _create_efficiency_data(self, y_pump):
        eff_from_x = self.pumptype.efficiency_from.value_m3ps
        eff_to_x = self.pumptype.efficiency_to.value_m3ps
        values = (eff_from_x, eff_to_x)
        return values

    def _figure_preconditions(self):
        rules = [
            self.hydr_cond.inflow_max.value_lps > 0,
            self.hydr_cond.inflow_min.value_lps > 0,
            self.pumptype.efficiency_from.value_lps > 0,
            self.pumptype.efficiency_to.value_lps > 0,
            self.hydr_cond.inflow_max.value_lps > self.hydr_cond.inflow_min.value_lps,
            self.pumptype.efficiency_to > self.pumptype.efficiency_from
        ]
        return all(rules)

    def _pump_char_ready(self):
        rules = [
            len(self.pumptype.characteristic.value) > 4
        ]
        return all(rules)


class ResultPumpsetCharData:

    def __init__(self, pumpset):
        self.pset = pumpset

    def prepare_data(self):
        data = {}
        data['x'] = self.create_x_array()
        data['pipeset_start'] = np.polynomial.polynomial.Polynomial(
            self.pset.wpoint_start.pipeset_poly)
        data['pipeset_stop'] = np.polynomial.polynomial.Polynomial(
            self.pset.wpoint_stop.pipeset_poly)
        data['pumpset'] = np.poly1d(np.flip(self.pset.pumpset_poly))
        data['workpoint_start'] = self.create_wpoint_data(self.pset.wpoint_start)
        data['workpoint_stop'] = self.create_wpoint_data(self.pset.wpoint_stop)
        data['pump_eff'] = self.create_efficiency_data(self.pset.pumpset_poly)
        return data

    def create_x_array(self):
        left = min(0.9 * self.pset.min_inflow.get_by_unit('m3ps'),
                   0.9 * self.pset.pumps_amount * self.pset.station.pump_type.efficiency_from.value_m3ps,
                   0.9 * self.pset.wpoint_stop.flow.value_m3ps)
        right = max(1.6 * self.pset.max_inflow.get_by_unit('m3ps'),
                    1.05 * self.pset.pumps_amount * self.pset.station.pump_type.efficiency_to.value_m3ps,
                    1.1 * self.pset.wpoint_stop.flow.value_m3ps)
        array = np.linspace(left, right, 10000)
        return array

    def create_wpoint_data(self, wpoint):
        flow = wpoint.flow.value_m3ps
        height = wpoint.height
        return (flow, height)

    def create_efficiency_data(self, y_pump):
        pumps_no = self.pset.pumps_amount
        eff_from_x = self.pset.station.pump_type.efficiency_from.value_m3ps * pumps_no
        eff_to_x = self.pset.station.pump_type.efficiency_to.value_m3ps * pumps_no
        values = (eff_from_x, eff_to_x)
        print('y_pump (eff): \n', y_pump)
        print('EFFICIENCY values: ', values)
        return values