import pytest


def test_1_unit_pumpset(station_2):
    station = station_2
    station.calculate('checking')
    assert station.pumpsystem.pumpsets[0].cyc_time > 480
    assert station.pumpsystem.pumpsets[0].cyc_time < 581


def test_1_unit_parallel_pipes(station_3):
    station_3.calculate('checking')
    pset = station_3.pumpsystem.pumpsets[0]
    assert pset.wpoint_start.height == pytest.approx(13.99, rel=0.05)
    assert pset.wpoint_start.flow.value_lps == pytest.approx(24.21, rel=.05)
    assert pset.ord_start == pytest.approx(95.97, abs=0.20)
    assert pset.wpoint_start.out_pipe_v == pytest.approx(0.48, abs=.02)


def test_3_units(station_4):
    station_4.calculate('checking')
    assert len(station_4.pumpsystem.pumpsets) == 2
    pset_1, pset_2 = station_4.pumpsystem.pumpsets
    assert pset_2.ord_start == pytest.approx(95.70, abs=0.20)
    assert pset_2.wpoint_start.height == pytest.approx(20.09, rel=.05)


def test_variable_reference(station_1):
    test_value = 34.6
    var_thru_get_var = station_1.ins_pipe.length.get_var('ord_terrain')
    var_thru_model = station_1.hydr_cond.ord_terrain
    assert var_thru_model is var_thru_get_var
    var_thru_get_var.set(test_value)
    assert var_thru_model is var_thru_get_var
    assert var_thru_get_var.get() == test_value
    assert var_thru_model.get() == test_value


def test_variable_singularity(station_1):
    """Has list of all variables, with names other than None, unique elements"""
    instances_all = station_1.ins_pipe.length._registry
    instances_with_name = []
    instances_with_unique_name = []
    for i in instances_all:
        if i.name is not None:
            instances_with_name.append(i)
            unique_flag = True
            for unique in instances_with_unique_name:
                if i.name == unique.name:
                    unique_flag = False
            if unique_flag:
                instances_with_unique_name.append(i)
    assert len(instances_with_unique_name) == len(instances_with_name)
    assert instances_with_unique_name == instances_with_name
