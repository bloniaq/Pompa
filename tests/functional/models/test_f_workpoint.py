import pompa.models.variables as v


def test_calculate(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    exp_height = 2
    exp_flow = v.FlowVariable(3000, 'lps')
    exp_geom_h = v.FloatVariable(6)
    exp_ins_pipe_speed = 0.5
    exp_out_pipe_speed = 0.25
    assert wpoint.height == exp_height
    assert wpoint.flow == exp_flow
    assert wpoint.geom_h == exp_geom_h
    assert wpoint.ins_pipe_v == exp_ins_pipe_speed
    assert wpoint.out_pipe_v == exp_out_pipe_speed
