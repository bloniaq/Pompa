import pytest

import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run(station_2):
    station_2.calculate()
    assert isinstance(
        station_2.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)


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


# below testing CHECKING if pumps fit in well


pumpsystems_check_area = [
    # shape, config, contour, well_dim, pumps, result
    ('round', 'singlerow', 0.3, 2.5, 8, True),
    ('round', 'singlerow', 0.3, 2.5, 9, False),
    ('round', 'optimal', 0.3, 1.7, 5, True),
    ('round', 'optimal', 0.3, 1.7, 6, False),
    ('rectangle', 'optimal', 0.3, (3.0, 4.0), 30, True),
    ('rectangle', 'optimal', 0.3, (3.0, 4.0), 31, False),
    ('rectangle', 'singlerow', 0.5, (2.2, 1.8), 4, True),
    ('rectangle', 'singlerow', 0.5, (2.2, 1.8), 5, False),
]


@pytest.mark.parametrize('shape, config, contour, well_dim, pumps, result',
                         pumpsystems_check_area)
def test_check_well_area(station_2, shape, config, contour, well_dim, pumps,
                         result):
    station_2.well.shape.set(shape)
    station_2.well.config.set(config)
    station_2.pump_type.contour.set(contour)
    if station_2.well.shape.value == 'round':
        station_2.well.diameter.set(well_dim)
    elif station_2.well.shape.value == 'rectangle':
        station_2.well.width.set(well_dim[0])
        station_2.well.length.set(well_dim[1])

    assert station_2.check_well_area_for_pumps(pumps) == result


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
    ('rectangle', 'optimal', 0.3, 5, (1.12, 2.50))  # minimal length
]


@pytest.mark.parametrize('shape, config, contour, pumps, result', pumpsystems_min_d)
def test_min_dimension(station_2, shape, config, contour, pumps, result):
    station_2.well.shape.set(shape)
    station_2.well.config.set(config)
    station_2.pump_type.contour.set(contour)
    assert station_2.min_well_dimension(pumps) == result
