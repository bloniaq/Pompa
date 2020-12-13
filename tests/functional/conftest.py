import pytest
import pompa.models.variables as v
import numpy as np
import pompa.models.pumpset


@pytest.fixture
def pompa0_pumpset():
    required_cycle_time = 480
    inflow = (v.FlowVariable(11, 'lps'), v.FlowVariable(22, 'lps'))
    pumpset_efficiency = (
        v.FlowVariable(23.5, 'lps'), v.FlowVariable(37, 'lps'))
    pumpset_poly = np.array([21.29551616, -165.30679483, -1601.8113366,
                             -6312.30558488])
    pipeset_poly = np.array([-9.31037900e+00, 1.39944923e+02, 5.37128457e+04,
                             0])
    ins_pipe_area = 0.0177
    out_pipe_area = 0.0314
    well_area = 4.91
    ord_upper_level = v.FloatVariable(148)
    ord_shutdown = v.FloatVariable(138.57)
    ord_inlet = v.FloatVariable(140)
    pumpset = pompa.models.pumpset.PumpSet(
        required_cycle_time, inflow, pumpset_efficiency, pipeset_poly,
        pumpset_poly, ins_pipe_area, out_pipe_area, well_area, ord_upper_level,
        ord_shutdown, ord_inlet)
    pumpset.expected_worst_inflow = v.FlowVariable(18, 'lps')
    return pumpset
