import pompa.models.pumpsystem
import pompa.models.variables as v
import numpy as np


def test_create(station_2):
    pumpsystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert pumpsystem is not None
    assert isinstance(pumpsystem.pumpsets, list)


def test_checking_method(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert psystem._checking_mode is not None


def test_calculation(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert psystem._calculate is not None
    assert len(psystem.pumpsets) > 0


def test_ord_shutdown(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    ord_bottom = station_2.hydr_cond.ord_bottom
    assert psystem.ord_shutdown(ord_bottom) == v.FloatVariable(139.04)

def test_reserve_pumps_economic(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    station_2.safety.set('economic')
    assert psystem._calc_reserve_pumps(1) == 1
    assert psystem._calc_reserve_pumps(2) == 1
    assert psystem._calc_reserve_pumps(3) == 1
    assert psystem._calc_reserve_pumps(4) == 1
    assert psystem._calc_reserve_pumps(5) == 1

def test_reserve_pumps_optimal(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert psystem._calc_reserve_pumps(1) == 1
    assert psystem._calc_reserve_pumps(2) == 1
    assert psystem._calc_reserve_pumps(3) == 2
    assert psystem._calc_reserve_pumps(4) == 2
    assert psystem._calc_reserve_pumps(5) == 3

def test_reserve_pumps_safe(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    station_2.safety.set('safe')
    assert psystem._calc_reserve_pumps(1) == 1
    assert psystem._calc_reserve_pumps(2) == 2
    assert psystem._calc_reserve_pumps(3) == 3
    assert psystem._calc_reserve_pumps(4) == 4
    assert psystem._calc_reserve_pumps(5) == 5
