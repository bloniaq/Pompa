import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run(station_2):
    station_2.calculate()
    assert isinstance(
        station_2.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)

class TestPipeFigureChecking:

    def test_preconditions_pass(self, station_2):
        assert station_2.figure_preconditions()

    def test_preconditions_fail_inflow_max_zero(self, station_2):
        station_2.hydr_cond.inflow_max.set(0, 'lps')
        assert not station_2.figure_preconditions()

    def test_preconditions_fail_inflow_min_zero(self, station_2):
        station_2.hydr_cond.inflow_min.set(0, 'lps')
        assert not station_2.figure_preconditions()

    def test_preconditions_fail_inflow_min_higher_than_max(self, station_2):
        station_2.hydr_cond.inflow_min.set(23, 'lps')
        assert not station_2.figure_preconditions()

    def test_geom_h_fig_pass(self, station_2):
        assert station_2.geom_h_figure_ready()

    def test_geom_h_fig_check_fail_highest_point_lower_than_upper(self, station_2):
        station_2.hydr_cond.ord_upper_level.set(150.3)
        assert not station_2.geom_h_figure_ready()

    def test_geom_h_fig_check_fail_highest_point_lower_than_outlet(self, station_2):
        station_2.hydr_cond.ord_outlet.set(150.3)
        assert not station_2.geom_h_figure_ready()

    def test_ins_pipe_fig_check_pass(self, station_2):
        assert station_2.ins_pipe_figure_ready()
    def test_ins_pipe_fig_check_fail_length_zero(self, station_2):
        station_2.ins_pipe.length.set(0)
        assert not station_2.ins_pipe_figure_ready()

    def test_ins_pipe_fig_check_fail_diameter_zero(self, station_2):
        station_2.ins_pipe.diameter.set(0)
        assert not station_2.ins_pipe_figure_ready()

    def test_ins_pipe_fig_check_fail_roughness_zero(self, station_2):
        station_2.ins_pipe.roughness.set(0)
        assert not station_2.ins_pipe_figure_ready()

    def test_out_pipe_fig_check_pass(self, station_2):
        assert station_2.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_length_zero(self, station_2):
        station_2.out_pipe.length.set(0)
        assert not station_2.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_diameter_zero(self, station_2):
        station_2.out_pipe.diameter.set(0)
        assert not station_2.out_pipe_figure_ready()

    def test_out_pipe_fig_check_fail_roughness_zero(self, station_2):
        station_2.out_pipe.roughness.set(0)
        assert not station_2.out_pipe_figure_ready()

