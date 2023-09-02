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

