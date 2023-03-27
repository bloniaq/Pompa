import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run(station_2):
    station_2.calculate()
    assert isinstance(
        station_2.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)

def test_min_well_dim_round_singlerow():
    station = pompa.models.station.Station()
    station.well.shape.set("round")
    station.well.config.set('singlerow')
    station.pump_type.contour.set(1)

    complete_pump_number = 2
    assert station.min_well_dimension(complete_pump_number) == 2.6

    complete_pump_number = 3
    assert station.min_well_dimension(complete_pump_number) == 3.9

    complete_pump_number = 2
    station.pump_type.contour.set(0.2)
    assert station.min_well_dimension(complete_pump_number) == 1.5

def test_min_well_dim_rect_singlerow():
    station = pompa.models.station.Station()
    station.well.shape.set("rectangle")
    station.well.config.set("singlerow")
    station.pump_type.contour.set(1)

    complete_pump_number = 2
    assert station.min_well_dimension(complete_pump_number) == (1.6, 2.6)

    complete_pump_number = 4
    assert station.min_well_dimension(complete_pump_number) == (1.6, 5.2)

    complete_pump_number = 2
    station.pump_type.contour.set(0.6)
    assert station.min_well_dimension(complete_pump_number) == (1.5, 1.8)

    station.pump_type.contour.set(0.3)
    assert station.min_well_dimension(complete_pump_number) == (1.5, 1.5)

    complete_pump_number = 4
    station.pump_type.contour.set(2)
    assert station.min_well_dimension(complete_pump_number) == (2.6, 9.2)

def test_min_well_dim_round_optimal():
    station = pompa.models.station.Station()
    station.well.shape.set("round")
    station.well.config.set("optimal")
    station.pump_type.contour.set(1)

    complete_pump_number = 4
    assert station.min_well_dimension(complete_pump_number) == 3.14

    station.pump_type.contour.set(1.6)
    complete_pump_number = 7
    assert station.min_well_dimension(complete_pump_number) == 5.70

    complete_pump_number = 9
    assert station.min_well_dimension(complete_pump_number) == 6.86

    station.pump_type.contour.set(0.2)
    complete_pump_number = 1
    assert station.min_well_dimension(complete_pump_number) == 1.5

def test_min_well_dim_rectangle_optimal():
    station = pompa.models.station.Station()
    station.well.shape.set("rectangle")
    station.well.config.set("optimal")
    station.pump_type.contour.set(1)

    complete_pump_number = 4
    assert station.min_well_dimension(complete_pump_number) == (2.6, 2.6)

    complete_pump_number = 3
    assert station.min_well_dimension(complete_pump_number) == (2.56, 2.56)

    complete_pump_number = 8
    assert station.min_well_dimension(complete_pump_number) == (3.81, 3.81)

    complete_pump_number = 10
    assert station.min_well_dimension(complete_pump_number) == (4.39, 4.39)

    station.pump_type.contour.set(0.2)
    complete_pump_number = 5
    assert station.min_well_dimension(complete_pump_number) == (1.50, 1.50)