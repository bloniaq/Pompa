import pytest
import numpy as np
import pompa.models.pipe as pipe
import pompa.models.pumpset as pumpset
import pompa.models.variables as v


@pytest.fixture
def friction_factor_laminar():
    diameter = v.FloatVariable(.200)
    roughness = v.FloatVariable(.001, digits=8)
    reynolds = 1000
    factor = pipe.FrictionFactor(diameter, roughness, reynolds)
    return factor


@pytest.fixture
def friction_factor_turbulent_smooth_cond():
    diameter = v.FloatVariable(.200)
    roughness = v.FloatVariable(.0001, digits=8)
    reynolds = 20000
    factor = pipe.FrictionFactor(diameter, roughness, reynolds)
    return factor


@pytest.fixture
def one_pump_pumpset(request):
    required_cycle_time = 100
    inflow = (v.FlowVariable(3, 'm3ps'), v.FlowVariable(7, 'm3ps'))
    pumpset_efficiency = (
        v.FlowVariable(5, 'm3ps'), v.FlowVariable(10, 'm3ps'))
    pipeset_poly = np.array([2, 1, 2, -1])
    pumpset_poly = np.array([-4, 2, -3, 1])
    ins_pipe_area = .2
    out_pipe_area = 1.5
    well_area = 3.14
    ord_upper_level = v.FloatVariable(22)
    ord_shutdown = v.FloatVariable(8)
    ord_inlet = v.FloatVariable(16)
    pset = pumpset.PumpSet(
        required_cycle_time, inflow, pumpset_efficiency, pipeset_poly,
        pumpset_poly, ins_pipe_area, out_pipe_area, well_area, ord_upper_level,
        ord_shutdown, ord_inlet)
    pset.expected_worst_inflow = v.FlowVariable(7, 'm3ps')
    return pset


@pytest.fixture
def more_pump_pumpset(request):
    required_cycle_time = 100
    inflow = (v.FlowVariable(3, 'm3ps'), v.FlowVariable(11, 'm3ps'))
    pumpset_efficiency = (
        v.FlowVariable(5, 'm3ps'), v.FlowVariable(10, 'm3ps'))
    pipeset_poly = np.array([2, 1, 2, -1])
    pumpset_poly = np.array([-4, 2, -3, 1])
    ins_pipe_area = .2
    out_pipe_area = 1.5
    well_area = 9.62
    ord_upper_level = v.FloatVariable(10)
    ord_shutdown = v.FloatVariable(1)
    ord_inlet = v.FloatVariable(5)
    ord_latter_pumpset_startup = v.FloatVariable(3)
    pset = pumpset.PumpSet(
        required_cycle_time, inflow, pumpset_efficiency, pipeset_poly,
        pumpset_poly, ins_pipe_area, out_pipe_area, well_area, ord_upper_level,
        ord_shutdown, ord_inlet, ord_latter_pumpset_startup)

    pset.expected_worst_inflow = v.FlowVariable(10, 'm3ps')
    return pset
