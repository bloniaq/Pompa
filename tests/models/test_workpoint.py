import pompa.models.workpoint
import pytest
import numpy as np
import pompa.models.variables as v


@pytest.fixture()
def workpoint_dummy_1pump():
    pumpset_amount = 1
    geometric_height = 6
    ins_pipe_crossec_area = 6
    out_pipe_crossec_area = 12
    pumpset_poly = np.array([-4, 2, -3, 1])
    pipeset_poly = np.array([2, 1, 2, -1])
    wpoint = pompa.models.workpoint.WorkPoint(
        pumpset_amount, geometric_height, ins_pipe_crossec_area,
        out_pipe_crossec_area, pumpset_poly, pipeset_poly)

    return wpoint


def test_init_class(workpoint_dummy_1pump):
    assert workpoint_dummy_1pump is not None


def test_init_attributes(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    assert wpoint.pumpset_amount == 1
    assert wpoint.geometric_height == 6
    assert wpoint.ins_pipe_crossec_area == 6
    assert wpoint.out_pipe_crossec_area == 12
    exp_pumpset_poly = np.array([-4, 2, -3, 1])
    exp_pipeset_hydr_poly = np.array([2, 1, 2, -1])
    np.testing.assert_equal(wpoint.pumpset_poly, exp_pumpset_poly)
    np.testing.assert_equal(wpoint.pipeset_hydr_poly, exp_pipeset_hydr_poly)


def test_speed(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    flow = v.FlowVariable(24000, 'lps')
    speed = wpoint._speed(flow)
    assert speed['ins_pipe'] == 4
    assert speed['out_pipe'] == 2


def test_full_loss_poly(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    exp_pipeset_poly = np.array([8, 1, 2, -1])
    result_poly = wpoint._full_loss_poly()
    assert isinstance(result_poly, np.ndarray)
    np.testing.assert_equal(result_poly, exp_pipeset_poly)


def test_calculate(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    exp_height = 2
    exp_flow = v.FlowVariable(3000, 'lps')
    exp_geom_h = 6
    exp_ins_pipe_speed = 0.5
    exp_out_pipe_speed = 0.25
    exp_tuple = (exp_height, exp_flow, exp_geom_h, exp_ins_pipe_speed,
                 exp_out_pipe_speed)
    assert wpoint.calculate() == exp_tuple
