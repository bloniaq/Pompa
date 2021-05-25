import pompa.models.pumpsystem
import pompa.models.variables as v
import numpy as np


def test_create(station_2):
    pumpsystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert pumpsystem is not None
    assert pumpsystem.mode is 'checking' or pumpsystem.mode is 'minimalisation'
    assert isinstance(pumpsystem.pumpsets, list)


def test_checking_method(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert psystem._checking_mode is not None


def test_calculation(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    assert psystem._calculate is not None
    psystem._calculate('checking')
    assert len(psystem.pumpsets) > 0


def test_ord_shutdown(station_2):
    psystem = pompa.models.pumpsystem.PumpSystem(station_2)
    ord_bottom = station_2.hydr_cond.ord_bottom
    assert psystem._ord_shutdown(ord_bottom) == v.FloatVariable(139.04)
