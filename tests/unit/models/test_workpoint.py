import numpy as np
import pompa.models.variables as v


def test_init_class(workpoint_dummy_1pump):
    assert workpoint_dummy_1pump is not None


def test_init_attributes(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    assert wpoint.geometric_height == v.FloatVariable(6)
    assert wpoint.ins_pipe_crossec_area == 6
    assert wpoint.out_pipe_crossec_area == 12
    exp_pumpset_poly = np.array([-4, 2, -3, 1])
    exp_pipeset_hydr_poly = np.array([2, 1, 2, -1])
    np.testing.assert_equal(wpoint.pumpset_poly, exp_pumpset_poly)
    np.testing.assert_equal(wpoint.pipeset_hydr_poly, exp_pipeset_hydr_poly)


def test_velocity(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    flow = v.FlowVariable(24000, 'lps')
    velocity = wpoint._velocity(flow)
    assert velocity['ins_pipe'] == 4
    assert velocity['out_pipe'] == 2


def test_full_loss_poly(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    exp_pipeset_poly = np.array([8, 1, 2, -1])
    result_poly = wpoint._full_loss_poly()
    assert isinstance(result_poly, np.ndarray)
    np.testing.assert_equal(result_poly, exp_pipeset_poly)
