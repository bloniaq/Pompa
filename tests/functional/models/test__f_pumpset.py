import pytest
import pompa.models.variables as v
from unittest.mock import patch


fixture_list = ['one_pump_pumpset', 'more_pump_pumpset']


@pytest.mark.parametrize('fixture', fixture_list)
@patch('pompa.models.pumpset.pompa.models.workpoint')
def test_workpoint_method(mock_wpoint, fixture, request):
    pumpset = request.getfixturevalue(fixture)
    current_ordinate = 6
    wpoint_calc_result = {}
    wpoint_calc_result['height'] = 8
    wpoint_calc_result['flow'] = v.FlowVariable(10)
    wpoint_calc_result['geom_h'] = pumpset._geom_height(current_ordinate)
    wpoint_calc_result['ins_pipe_speed'] = 6
    wpoint_calc_result['out_pipe_speed'] = 5
    mock_wpoint.WorkPoint().calculate.return_value = wpoint_calc_result
    assert pumpset._workpoint(current_ordinate) == wpoint_calc_result


"""
def test_calculate_one_pump(pompa0_pumpset):
    pumpset = pompa0_pumpset
    # Results
    result = {}
    result['working_time'] = 247
    result['layover_time'] = 237
    result['cycle_time'] = 484
    result['useful_velo'] = 4.3
    result['start_ordinate'] = 139.80
    exp_start_wpoint = {'height': 12.99,
                        'geom_h': 8.26,
                        'flow': v.FlowVariable(36.16, 'lps'),
                        'out_pipe_speed': 1.15,
                        'ins_pipe_speed': 2.04}
    exp_stop_wpoint = {'height': 13.47,
                       'geom_h': 9.13,
                       'flow': v.FlowVariable(34.50, 'lps'),
                       'out_pipe_speed': 1.1,
                       'ins_pipe_speed': 1.95}
    result['stop_wpoint'] = exp_stop_wpoint
    result['start_wpoint'] = exp_start_wpoint
    result['efficiency_from'] = v.FlowVariable(23.5, 'lps')
    result['efficiency_to'] = v.FlowVariable(37, 'lps')
    result['worst_inflow'] = v.FlowVariable(18, 'lps')

    assert pumpset.calculate() == result
"""