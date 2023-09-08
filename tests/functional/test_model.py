import pytest

import pompa.models.pumpsystem


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
    assert pset_2.ord_start == pytest.approx(95.70, abs=0.21)
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


def test_minimal_rectangle_well_dimensions_for_optimal_config(app_fixture):

    with app_fixture as app:
        filepath = 'tests/scenarios/15-FIX-minimalne_wymiary_studni_prostok.DAN'
        app.load_file(filepath, 'lps')
        s = app.model
        ps = pompa.models.pumpsystem.PumpSystem(s)
        assert s.min_well_dimension(ps.all_pumps) == (2.43, 2.6)


def test_volumes(app_fixture):

    with app_fixture as app:
        filepath = 'tests/scenarios/16-objetosci charakterystyczne.DAN'
        app.load_file(filepath, 'lps')
        s = app.model
        ps = pompa.models.pumpsystem.PumpSystem(s)
        # Długość pompowni.....................L = 2.0[m]
        # Szerokość pompowni...................B = 2.5[m]
        # Rzędna terenu......................... 100.0[m]
        # Rzędna dopływu ścieków................ 96.6[m]
        # Rzędna wylotu ścieków / przejście
        # osi rury przez ścianę pompowni / .......97.2[m]
        # Min. wysokość ścieków w  pompowni.....    0.3    [m]
        # Rzędna dopływu ścieków................ 96.6[m]
        # Rzędna dna pompowni................... 94.54[m]
        # Rzędna wyłączenia się pomp............ 94.84[m]
        # Objętość całkowita pompowni..........Vc = 27.3[m3]
        # Objętość użyteczna pompowni..........Vu = 5.95[m3]
        # Objętość rezerwowa pompowni..........Vr = 2.85[m3]
        # Objętość martwa pompowni.............Vm = 1.5[m3]
        #
        # Vu / Vc = 21.8 %
        # Vr / Vu = 47.9 %
        # Vr / Vc = 10.4 %
        # Vm / Vc = 5.5 %
        #
        # Obj. użyt. wyzn. przez pompę......Vu=   3.25    [m3]
        # Rzędna włączenia pompy..............   95.49     [m]
        # Obj. użyt. wyzn. przez pompę......Vu=    2.7    [m3]
        # Rzędna włączenia pompy..............   96.03     [m]

        assert False
