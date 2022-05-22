import pompa.models.pumpset
import pompa.models.variables as v
import pompa.models.workpoint
import numpy as np
import pytest
from unittest.mock  import Mock


@pytest.fixture
def s2_pumpset(station_2):
    ord_shutdown = v.FloatVariable(138.87)
    pumpset = pompa.models.pumpset.PumpSet(station_2, ord_shutdown)
    return pumpset


def test_pumpset_init(s2_pumpset):
    assert s2_pumpset is not None
    assert s2_pumpset._well_area == pytest.approx(4.9, abs=0.02)
    assert s2_pumpset._req_cycle_time.value == 480

    assert s2_pumpset.ord_stop == 138.87


def test_pumpset_layover_time(s2_pumpset, s2_pumpset_points):
    worst_inflow = v.FlowVariable(12.59, 'lps')
    assert s2_pumpset._layover_time(
        s2_pumpset_points, worst_inflow) == pytest.approx(273, abs=1)


def test_pumpset_working_time(s2_pumpset, s2_pumpset_points):
    worst_inflow = v.FlowVariable(12.59, 'lps')
    assert s2_pumpset._working_time(
        s2_pumpset_points, worst_inflow) == pytest.approx(273, abs=1)


def test_pumpset_cycle_time(s2_pumpset, s2_pumpset_points):
    worst_inflow = v.FlowVariable(12.59, 'lps')
    assert s2_pumpset._cycle_times(
        s2_pumpset_points, worst_inflow)[0] == pytest.approx(545, abs=2)


@pytest.mark.parametrize('ord_, height, flow_val, geom_h, ins_p_v, out_p_v', [
    (139.04, 12.19, 24.52, 9.08, 1.35, .76),
    (139.64, 11.90, 25.67, 8.48, 1.41, .79),
    (140.24, 11.61, 26.79, 7.88, 1.52, .85)])
def test_pumpset_workpoint_interface(ord_, height, flow_val, geom_h, ins_p_v,
                                     out_p_v, s2_pumpset):
    ordinate = v.FloatVariable(ord_)
    wpoint = s2_pumpset._workpoint(ordinate)
    assert wpoint is not None
    assert wpoint.height == pytest.approx(height, rel=.02)
    assert wpoint.flow.value_lps == pytest.approx(flow_val, rel=.02)
    assert wpoint.geom_h == geom_h
    assert wpoint.ins_pipe_v == pytest.approx(ins_p_v, rel=.05)
    assert wpoint.out_pipe_v == pytest.approx(out_p_v, rel=.05)


def test_pumpset_geom_height(s2_pumpset):
    ordinate = v.FloatVariable(139.44)
    assert s2_pumpset._geom_height(ordinate) == 8.68


def test_worst_inflow(s2_pumpset, s2_pumpset_points):
    assert s2_pumpset._worst_inflow(
        s2_pumpset_points).value_lps == pytest.approx(12.59, rel=.02)


def test_worst_inflow_multiple_pumps(station_4_psets):
    station, pset_1, pset_2, pset_3 = station_4_psets
    assert pset_2.worst_inflow.value_lps > pset_1.wpoint_start.flow.value_lps
    assert pset_3.worst_inflow.value_lps > pset_2.wpoint_start.flow.value_lps


def test_min_inflow(station_4_psets):
    station, pset_1, pset_2, pset_3 = station_4_psets

    assert pset_2._min_inflow.value_lps == pytest.approx(max(
        pset_1.wpoint_start.flow.value_lps + .1,
        station.hydr_cond.inflow_min.value_lps), rel=.0001)


def test_calculate(s2_pumpset):
    s2_pumpset._ORD_STEP = 0.1
    exp_dict = {
        'cyc_time': 545,
        'wor_time': 273,
        'lay_time': 273,
        'vol_u': 3.43,
        'wpoint_stop': s2_pumpset._workpoint(v.FloatVariable(139.04)),
        'ord_start': 139.74,
        'wpoint_start': s2_pumpset._workpoint(v.FloatVariable(139.74)),
        'worst_inflow': v.FlowVariable(12.59, 'lps')}
    s2_pumpset._calculate()
    assert s2_pumpset.cyc_time == pytest.approx(exp_dict['cyc_time'], rel=.02)
    assert s2_pumpset.wor_time == pytest.approx(exp_dict['wor_time'], rel=.015)
    assert s2_pumpset.lay_time == pytest.approx(exp_dict['lay_time'], rel=.015)
    assert s2_pumpset.vol_u == pytest.approx(exp_dict['vol_u'], rel=.01)
    assert s2_pumpset.ord_start == pytest.approx(
        exp_dict['ord_start'], rel=.002)
    assert s2_pumpset.worst_inflow.value_lps == pytest.approx(
        exp_dict['worst_inflow'].value_lps, rel=.02)


def test_optimal_range(station_4_psets):
    station, pset_1, pset_2, pset_3 = station_4_psets
    assert pset_2.opt_range[0] == station.pump_type.efficiency_from * 2
    assert pset_2.opt_range[1] == station.pump_type.efficiency_to * 2
