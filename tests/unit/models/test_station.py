import pytest

import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run(station_2):
    station_2.calculate()
    assert isinstance(
        station_2.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)


def test_check_well_area_station_2_round_singlerow(station_2):
    # essential_data_s2 = {
    #     'contour': 0.3,
    #     'well_diam': 2.5,
    #     'shape': 'round',
    #     'config': 'singlerow',
    #     'pump_contour': pump_c
    #     }
    all_pumps_count = 8
    assert station_2.check_well_area_for_pumps(all_pumps_count)
    all_pumps_count = 9
    assert not station_2.check_well_area_for_pumps(all_pumps_count)


def test_check_well_area_station_2_round_optimal(station_2):
    s = station_2
    s.well.config.set('optimal')
    s.well.diameter.set(1.7)

    # essential_data = {
    #     'contour': 0.3,
    #     'well_diam': 1.7,
    #     'shape': 'round',
    #     'config': 'optimal',
    #     'pump_contour': pump_c
    #     }

    all_pumps_count = 5
    assert s.check_well_area_for_pumps(all_pumps_count)
    all_pumps_count = 6
    assert not s.check_well_area_for_pumps(all_pumps_count)


def test_check_well_area_station_2_rectangular_optimal(station_2):
    s = station_2
    s.well.shape.set('rectangle')
    s.well.width.set(3)
    s.well.length.set(4)
    s.well.config.set('optimal')

    # essential_data = {
    #     'contour': 0.3,
    #     'well_width': 3,
    #     'well_length': 4,
    #     'shape': 'rectangle',
    #     'config': 'optimal',
    #     'pump_contour': safe_pump_c=0.6
    #     }

    all_pumps_count = 30
    assert s.check_well_area_for_pumps(all_pumps_count)
    all_pumps_count = 31
    assert not s.check_well_area_for_pumps(all_pumps_count)


def test_check_well_area_station_2_rectangular_singlerow(station_2):
    s = station_2
    s.well.shape.set('rectangle')
    s.well.width.set(2.2)
    s.well.length.set(1.8)
    s.pump_type.contour.set(0.5)
    s.well.config.set('singlerow')

    # essential_data = {
    #     'contour': 0.5,
    #     'well_width': 2.2,
    #     'well_length': 1.8,
    #     'shape': 'rectangle',
    #     'config': 'singlerow',
    #     'pump_contour': pump_c=0.5
    #     }

    all_pumps_count = 4
    assert s.check_well_area_for_pumps(all_pumps_count)
    all_pumps_count = 5
    assert not s.check_well_area_for_pumps(all_pumps_count)


def test_validate_dead_volume_under_inlet(station_2):
    s = station_2
    s.pump_type.suction_level.set(0.6)
    assert s.validate_dead_volume_under_inlet()
    s.hydr_cond.ord_inlet.set(139.11)
    assert not s.validate_dead_volume_under_inlet()


def test_min_ins_pipe_length(station_2):
    s = station_2
    assert s.validate_min_ins_pipe_length()
    s.ins_pipe.length.set(2)
    assert not s.validate_min_ins_pipe_length()

# below testing CALCULATIONS of minimal dimensions


pumpsystems_min_d = [
    # shape, config, contour, pumps, result
    ('round', 'singlerow', 0.3, 8, 2.4),
    ('round', 'singlerow', 0.3, 2, 1.5),  # minimal diameter
    ('round', 'singlerow', 1, 2, 2.6),
    ('round', 'singlerow', 1, 3, 3.9),
    ('rectangle', 'singlerow', 1, 2, (1.8, 2.6)),
    ('rectangle', 'singlerow', 1, 4, (1.8, 5.2)),
    ('rectangle', 'singlerow', 0.6, 2, (1.2, 2.5)),  # minimal length, flip w&l
    ('rectangle', 'singlerow', 0.3, 2, (1, 2.5)),  # minimal width + length
    ('rectangle', 'singlerow', 2, 4, (2.8, 9.2)),
    ('round', 'optimal', 1, 4, 3.14),
    ('round', 'optimal', 1.6, 7, 5.70),
    ('round', 'optimal', 1.6, 9, 6.86),
    ('round', 'optimal', 0.2, 1, 1.5),  # minimal diameter
    ('rectangle', 'optimal', 1, 4, (2.43, 3.25)),
    ('rectangle', 'optimal', 1, 3, (2.43, 2.60)),
    ('rectangle', 'optimal', 0.7, 5, (1.87, 3.00)),
    ('rectangle', 'optimal', 0.7, 6, (1.87, 3.50)),
    ('rectangle', 'optimal', 0.7, 8, (1.87, 4.50)),
    ('rectangle', 'optimal', 0.7, 9, (1.87, 5.00)),
    ('rectangle', 'optimal', 0.7, 10, (1.87, 5.50)),
    ('rectangle', 'optimal', 0.2, 5, (1.00, 2.50)),  # minimal width + length
    ('rectangle', 'optimal', 0.3, 5, (1.12, 2.50)),  # minimal length

]


@pytest.mark.parametrize('shape, config, contour, pumps, result', pumpsystems_min_d)
def test_min_dimension(station_2, shape, config, contour, pumps, result):
    station_2.well.shape.set(shape)
    station_2.well.config.set(config)
    station_2.pump_type.contour.set(contour)
    assert station_2.min_well_dimension(pumps) == result
