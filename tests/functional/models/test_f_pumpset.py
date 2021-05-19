import pytest
import pompa.models.variables as v


def test_1_unit_pumpset():
    pass

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