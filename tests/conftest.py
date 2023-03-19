import pytest
import numpy as np
import pompa.models.pipe as pipe
import pompa.models.pumpset as pumpset
from pompa.models.station import Station
from collections import OrderedDict, namedtuple
import pompa.models.variables as v
import pompa.models.workpoint
import pompa.application as app_module


@pytest.fixture(autouse=True)
def clean_model_variable_registry():
    v.Variable.clean_registry()


@pytest.fixture
def station_1(request):
    station = Station()
    safety_coeff = 1.4
    # input values:
    station.well.config.set('optimal')
    station.well.diameter.set(2.5)
    station.hydr_cond.ord_terrain.set(145)
    station.hydr_cond.ord_inlet.set(140)
    station.hydr_cond.ord_highest_point.set(148.12)
    station.hydr_cond.ord_upper_level.set(146.7)
    station.hydr_cond.reserve_height.set(0.2)
    station.hydr_cond.inflow_min.set(80, 'm3ph')
    station.hydr_cond.inflow_max.set(safety_coeff * 80, 'm3ph')
    station.ins_pipe.length.set(6)
    station.ins_pipe.diameter.set(0.15)
    station.ins_pipe.roughness.set(0.002)
    station.ins_pipe.resistances.set([3.38])
    station.out_pipe.length.set(732)
    station.out_pipe.diameter.set(0.2)
    station.out_pipe.roughness.set(0.002)
    station.out_pipe.resistances.set([0])
    station.pump_type.cycle_time.set(480)
    station.pump_type.contour.set(0.5)
    station.pump_type.suction_level.set(0.3)
    station.pump_type.efficiency_from.set(90, 'm3ph')
    station.pump_type.efficiency_to.set(110, 'm3ph')
    station.pump_type.characteristic.add_point(60, 14)
    station.pump_type.characteristic.add_point(70, 13.5)
    station.pump_type.characteristic.add_point(80, 12.8)
    station.pump_type.characteristic.add_point(90, 12)
    station.pump_type.characteristic.add_point(100, 11.3)
    station.pump_type.characteristic.add_point(110, 10.6)
    station.pump_type.characteristic.add_point(120, 9.8)
    station.pump_type.characteristic.add_point(130, 9)
    station.pump_type.characteristic.add_point(140, 8)

    return station


@pytest.fixture
def station_2():
    station = Station()

    # Pump Type
    station.pump_type.suction_level.set(0.3)
    station.pump_type.efficiency_from.set(23.5, 'lps')
    station.pump_type.efficiency_to.set(37, 'lps')
    station.pump_type.cycle_time.set(480)

    # Pump Characteristic
    station.pump_type.characteristic.add_point(16.7, 14, 'lps')
    station.pump_type.characteristic.add_point(19.4, 13.5, 'lps')
    station.pump_type.characteristic.add_point(22.2, 12.8, 'lps')
    station.pump_type.characteristic.add_point(25, 12, 'lps')
    station.pump_type.characteristic.add_point(27.8, 11.3, 'lps')
    station.pump_type.characteristic.add_point(30.6, 10.6, 'lps')
    station.pump_type.characteristic.add_point(33.3, 9.8, 'lps')
    station.pump_type.characteristic.add_point(36.1, 9, 'lps')
    station.pump_type.characteristic.add_point(38.9, 8, 'lps')

    # Well
    station.well.shape.set('round')
    station.well.diameter.set(2.5)

    # Hydraulic Conditions
    station.hydr_cond.ord_bottom.set(138.74)
    station.hydr_cond.ord_terrain.set(142)
    station.hydr_cond.ord_upper_level.set(148.12)
    station.hydr_cond.ord_highest_point.set(150.24)
    station.hydr_cond.ord_inlet.set(140)
    station.hydr_cond.ord_outlet.set(141)
    station.hydr_cond.inflow_min.set(11, 'lps')
    station.hydr_cond.inflow_max.set(22, 'lps')

    # Inside Pipe
    station.ins_pipe.length.set(7)
    station.ins_pipe.diameter.set(.150)
    station.ins_pipe.roughness.set(.0008)
    station.ins_pipe.resistances.set([0.27, 0.27, 0.6, 0.2, 2, 0.04])

    # Outside Pipe
    station.out_pipe.length.set(732)
    station.out_pipe.diameter.set(.200)
    station.out_pipe.roughness.set(0.0005)
    station.out_pipe.resistances.set([])
    return station


@pytest.fixture()
def s2_pumpset_points(station_2):
    ord_shutdown = v.FloatVariable(138.87)
    v.Variable.clean_registry()
    pset = pumpset.PumpSet(station_2, ord_shutdown)
    wp = pset._workpoint
    flow = v.FlowVariable
    Point = namedtuple('Point', ['wpoint', 'it_v', 'it_eff', 'e_time'])
    points = OrderedDict()
    points['139.04'] = Point(wp(v.FloatVariable(139.04)), 0, None, 0)
    points['139.14'] = Point(wp(v.FloatVariable(139.14)), 0.49, flow(0.0246, 'm3ps'), 19.93)
    points['139.24'] = Point(wp(v.FloatVariable(139.24)), 0.49, flow(0.0248, 'm3ps'), 19.78)
    points['139.34'] = Point(wp(v.FloatVariable(139.34)), 0.49, flow(0.0250, 'm3ps'), 19.62)
    points['139.44'] = Point(wp(v.FloatVariable(139.44)), 0.49, flow(0.0252, 'm3ps'), 19.47)
    points['139.54'] = Point(wp(v.FloatVariable(139.54)), 0.49, flow(0.0254, 'm3ps'), 19.33)
    points['139.64'] = Point(wp(v.FloatVariable(139.64)), 0.49, flow(0.0256, 'm3ps'), 19.18)
    points['139.74'] = Point(wp(v.FloatVariable(139.74)), 0.49, flow(0.0258, 'm3ps'), 19.04)
    return points


@pytest.fixture()
def station_3():
    station = pompa.models.station.Station()

    # Pump Type
    station.pump_type.suction_level.set(0.3)
    station.pump_type.efficiency_from.set(15, 'lps')
    station.pump_type.efficiency_to.set(19, 'lps')
    station.pump_type.cycle_time.set(600)

    # Pump Characteristic
    station.pump_type.characteristic.add_point(12, 19.6, 'lps')
    station.pump_type.characteristic.add_point(13, 19.2, 'lps')
    station.pump_type.characteristic.add_point(14, 18.9, 'lps')
    station.pump_type.characteristic.add_point(15, 18.6, 'lps')
    station.pump_type.characteristic.add_point(16, 18.4, 'lps')
    station.pump_type.characteristic.add_point(17, 18.1, 'lps')
    station.pump_type.characteristic.add_point(18, 17.7, 'lps')
    station.pump_type.characteristic.add_point(19, 17.2, 'lps')
    station.pump_type.characteristic.add_point(20, 16.6, 'lps')
    station.pump_type.characteristic.add_point(23, 0, 'lps')

    # Well
    station.well.shape.set('round')
    station.well.diameter.set(2.0)

    # Hydraulic Conditions
    station.hydr_cond.ord_bottom.set(94.54)
    station.hydr_cond.ord_upper_level.set(105)
    station.hydr_cond.ord_inlet.set(96)
    station.hydr_cond.inflow_min.set(10, 'lps')
    station.hydr_cond.inflow_max.set(20, 'lps')

    # Inside Pipe
    station.ins_pipe.length.set(6)
    station.ins_pipe.diameter.set(.110)
    station.ins_pipe.roughness.set(.0008)
    station.ins_pipe.resistances.set([0.27, 0.27, 0.6, 0.2, 2, 0.04])

    # Outside Pipe
    station.out_pipe.length.set(2500)
    station.out_pipe.diameter.set(.180)
    station.out_pipe.roughness.set(0.0005)
    station.out_pipe.resistances.set([])

    station.out_pipes_no.set(2)

    return station


@pytest.fixture()
def station_4(station_3):
    station = station_3
    station.out_pipes_no.set(1)

    return station


@pytest.fixture()
def station_4_psets(station_4):
    station = station_4
    station.calculate('checking')
    pset_1, pset_2, pset_3 = station_4.pumpsystem.pumpsets
    return station, pset_1, pset_2, pset_3


@pytest.fixture()
def workpoint_dummy_1pump():
    geometric_height = 6
    ins_pipe_crossec_area = 6
    out_pipe_crossec_area = 12
    pumpset_poly = np.array([-4, 2, -3, 1])
    pipeset_poly = np.array([2, 1, 2, -1])
    wpoint = pompa.models.workpoint.WorkPoint(
        geometric_height, ins_pipe_crossec_area,
        out_pipe_crossec_area, pumpset_poly, pipeset_poly)

    return wpoint


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
def mocked_vm_variables_data(mocker):
    variables_data = app_module.Application._init_variables()
    for v in variables_data:
        v.modelvar = mocker.MagicMock()
    return variables_data