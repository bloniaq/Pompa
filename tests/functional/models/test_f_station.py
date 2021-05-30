import pytest


def test_1_unit_pumpset(station_2):
    station = station_2
    station.calculate('checking')
    assert station.pumpsystem.pumpsets[0].cyc_time > 480
    assert station.pumpsystem.pumpsets[0].cyc_time < 581


def test_1_unit_parallel_pipes(station_3):
    station_3.calculate('checking')
    pset = station_3.pumpsystem.pumpsets[0]
    assert pset.wpoint_start.height == pytest.approx(13.86, rel=.01)
    assert pset.wpoint_start.flow.value_lps == pytest.approx(22.63, rel=.01)
    assert pset.ord_start == pytest.approx(95.90, rel=.001)
    assert pset.wpoint_start.out_pipe_v == pytest.approx(0.44, abs=.02)


def test_3_units(station_4):
    station_4.calculate('checking')
    assert len(station_4.pumpsystem.pumpsets) == 3
    pset_1, pset_2, pset_3 = station_4.pumpsystem.pumpsets
    assert pset_3.ord_start == pytest.approx(95.57, rel=.001)
    assert pset_3.wpoint_start.height == pytest.approx(23.35, rel=.02)
