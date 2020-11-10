import pompa.models.pumpsystem
import pompa.models.variables as v
import numpy as np


def create_pumpsystem_of_station_fixture(station):
    pumpsystem = pompa.models.pumpsystem.PumpSystem(
        station.well,
        station.ins_pipe,
        station.out_pipe,
        station.pump_type,
        station.hydr_cond)
    return pumpsystem


def test_create(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    assert pumpsystem is not None


def test_checking_method(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    assert pumpsystem.checking is not None


def test_checking_loop_ending(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    pumpsystem.hydr_cond.inflow_max.set(66)
    pumpsystem.checking()
    assert len(pumpsystem.pumpsets) == 3


def test_stop_ordinate(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    pumpsystem.pump_type.suction_level.set(0.3)
    bottom_ordinate = v.FloatVariable(31.56)
    expected_ordinate = v.FloatVariable(31.86)
    assert pumpsystem._stop_ordinate(bottom_ordinate) == expected_ordinate


def test_flow_array(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    minimal_flow = v.FlowVariable(8, 'lps')
    maximal_flow = v.FlowVariable(1.5 * 40, 'lps')
    expected_array = np.linspace(
        minimal_flow.value_m3ps, maximal_flow.value_m3ps, 200)
    assert isinstance(pumpsystem.flow_array, np.ndarray)
    np.testing.assert_equal(pumpsystem.flow_array, expected_array)


def test_pipes_polynomial(station_1):
    pumpsystem = create_pumpsystem_of_station_fixture(station_1)
    pumpsystem.flow_array = np.array(
        [0.022, 0.024, 0.026, 0.029, 0.031, 0.033, 0.036])
    exp_array = np.array(
        [9.653, -25.435, 6357.133, -7846.074])
    np.testing.assert_almost_equal(
        pumpsystem._pipes_dyn_loss_polynomial(), exp_array, decimal=3)
