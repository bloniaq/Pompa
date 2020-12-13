import pompa.models.pumpset
import pompa.models.variables as v
import pompa.models.workpoint
import numpy as np
from unittest.mock import Mock
import pytest


fixture_list = ['one_pump_pumpset', 'more_pump_pumpset']


@pytest.mark.parametrize('fixture', fixture_list)
def test_init(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    assert isinstance(pumpset, pompa.models.pumpset.PumpSet)


@pytest.mark.parametrize('fixture', fixture_list)
def test_attributes_types(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    assert isinstance(pumpset.required_cycle_time, int)
    assert isinstance(pumpset.inflow, tuple)
    assert isinstance(pumpset.inflow[0], v.FlowVariable)
    assert isinstance(pumpset.inflow[1], v.FlowVariable)
    assert isinstance(pumpset.pumpset_efficiency, tuple)
    assert isinstance(pumpset.pumpset_efficiency[0], v.FlowVariable)
    assert isinstance(pumpset.pumpset_efficiency[1], v.FlowVariable)
    assert isinstance(pumpset.pipeset_poly, np.ndarray)
    assert isinstance(pumpset.pumpset_poly, np.ndarray)
    assert isinstance(pumpset.ins_pipe_area, float)
    assert isinstance(pumpset.out_pipe_area, float)
    assert isinstance(pumpset.well_area, float)
    assert isinstance(pumpset.ord_upper_level, v.FloatVariable)
    assert isinstance(pumpset.ord_shutdown, v.FloatVariable)
    assert isinstance(pumpset.ord_inlet, v.FloatVariable)
    assert isinstance(pumpset.ord_latter_pumpset_startup, v.FloatVariable)


@pytest.mark.parametrize('fixture', fixture_list)
def test_geometric_height(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    checked_ordinate = v.FloatVariable(3)
    expected_result = pumpset.ord_upper_level - checked_ordinate
    assert pumpset._geom_height(checked_ordinate) == expected_result


@pytest.mark.parametrize('fixture', fixture_list)
def test_velocity(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    checked_height = .1
    expected_result = round(pumpset.well_area * checked_height, 2)
    assert pumpset._velocity(checked_height) == expected_result


@pytest.mark.parametrize('fixture', fixture_list)
def test_current_average_eff(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    workpoint_last = {}
    workpoint_last_but_one = {}
    workpoint_last_but_one['flow'] = v.FlowVariable(5, 'm3ph')
    workpoint_last['flow'] = v.FlowVariable(15, 'm3ph')
    pumpset.workpoints = [workpoint_last_but_one, workpoint_last]
    expected_result = v.FlowVariable(10, 'm3ph')
    assert pumpset._current_average_eff() == expected_result


@pytest.mark.parametrize('fixture', fixture_list)
def test_absolute_average_eff(fixture, request):
    pumpset = request.getfixturevalue(fixture)
    pumpset.efficiencys = [
        v.FlowVariable(11, 'lps'),
        v.FlowVariable(12, 'lps'),
        v.FlowVariable(13, 'lps'),
        v.FlowVariable(14, 'lps'),
        v.FlowVariable(15, 'lps')]
    expected_result = v.FlowVariable(13, 'lps')
    assert pumpset._absolute_average_eff() == expected_result


def test_worst_inflow_between_inflow(one_pump_pumpset):
    pumpset = one_pump_pumpset
    average_efficiency = v.FlowVariable(8, 'm3ps')
    expected_result = v.FlowVariable(4, 'm3ps')
    assert pumpset._worst_inflow(average_efficiency) == expected_result


def test_worst_inflow_outside_inflow(one_pump_pumpset):
    pumpset = one_pump_pumpset
    average_efficiency = v.FlowVariable(17, 'm3ps')
    expected_result = v.FlowVariable(7, 'm3ps')
    assert pumpset._worst_inflow(average_efficiency) == expected_result


@pytest.mark.parametrize('avg_flow, exp_times', [
    (v.FlowVariable(15, 'm3ps'), (12, 24)),
    (v.FlowVariable(20, 'm3ps'), (12, 12))])
def test_update_cycle_times(one_pump_pumpset, avg_flow, exp_times):
    pumpset = one_pump_pumpset
    pumpset._velocity = Mock()
    pumpset._velocity.return_value = 120
    pumpset.worst_inflow = v.FlowVariable(10, 'm3ps')
    pumpset._update_cycle_times(avg_flow)
    assert pumpset.layover_time == exp_times[0]
    assert pumpset.working_time == exp_times[1]
    assert pumpset.cycle_time == sum(list(exp_times))


def test_useful_velo_one_pump(one_pump_pumpset):
    pumpset = one_pump_pumpset
    start_ord = v.FloatVariable(12)
    assert pumpset._useful_velo(start_ord) == 12.56


def test_useful_velo_more_pumps(more_pump_pumpset):
    pumpset = more_pump_pumpset
    start_ord = v.FloatVariable(4)
    assert pumpset._useful_velo(start_ord) == 9.62
