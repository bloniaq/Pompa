import pompa.models.variables as v


def test_calculate(workpoint_dummy_1pump):
    wpoint = workpoint_dummy_1pump
    exp_height = 2
    exp_flow = v.FlowVariable(3000, 'lps')
    exp_geom_h = v.FloatVariable(6)
    exp_ins_pipe_speed = 0.5
    exp_out_pipe_speed = 0.25
    exp_dict = {'height': exp_height, 'flow': exp_flow, 'geom_h': exp_geom_h,
                'ins_pipe_velo': exp_ins_pipe_speed,
                'out_pipe_velo': exp_out_pipe_speed}
    assert wpoint.calculate() == exp_dict
