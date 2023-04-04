import pytest
import pompa.models.figures_data as fig_data


@pytest.fixture
def data_collector(station_2):
    chart_data = fig_data.ChartData(station_2)
    return chart_data

class TestPipeFigureChecking:

    def test_preconditions_pass(self, data_collector):
        assert data_collector.pipe_chart.figure_preconditions()

    def test_preconditions_fail_inflow_max_zero(self, data_collector):
        data_collector.station.hydr_cond.inflow_max.set(0, 'lps')
        assert not data_collector.pipe_chart.figure_preconditions()

    def test_preconditions_fail_inflow_min_zero(self, data_collector):
        data_collector.station.hydr_cond.inflow_min.set(0, 'lps')
        assert not data_collector.pipe_chart.figure_preconditions()

    def test_preconditions_fail_inflow_min_higher_than_max(self, data_collector):
        data_collector.station.hydr_cond.inflow_min.set(23, 'lps')
        assert not data_collector.pipe_chart.figure_preconditions()

    def test_geom_h_fig_pass(self, data_collector):
        assert data_collector.pipe_chart.geom_h_figure_ready()

    def test_geom_h_fig_check_fail_highest_point_lower_than_outlet(self, data_collector):
        data_collector.station.hydr_cond.ord_outlet.set(150.3)
        assert not data_collector.pipe_chart.geom_h_figure_ready()

    def test_ins_pipe_fig_check_pass(self, data_collector):
        assert data_collector.pipe_chart.ins_pipe_figure_ready()

    def test_ins_pipe_fig_check_fail_length_zero(self, data_collector):
        data_collector.station.ins_pipe.length.set(0)
        assert not data_collector.pipe_chart.ins_pipe_figure_ready()

    def test_ins_pipe_fig_check_fail_diameter_zero(self, data_collector):
        data_collector.station.ins_pipe.diameter.set(0)
        assert not data_collector.pipe_chart.ins_pipe_figure_ready()

    def test_ins_pipe_fig_check_fail_roughness_zero(self, data_collector):
        data_collector.station.ins_pipe.roughness.set(0)
        assert not data_collector.pipe_chart.ins_pipe_figure_ready()

    def test_out_pipe_fig_check_pass(self, data_collector):
        assert data_collector.pipe_chart.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_length_zero(self, data_collector):
        data_collector.station.out_pipe.length.set(0)
        assert not data_collector.pipe_chart.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_diameter_zero(self, data_collector):
        data_collector.station.out_pipe.diameter.set(0)
        assert not data_collector.pipe_chart.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_roughness_zero(self, data_collector):
        data_collector.station.out_pipe.roughness.set(0)
        assert not data_collector.pipe_chart.out_pipe_figure_ready()