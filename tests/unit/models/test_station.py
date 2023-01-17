import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run(station_2):
    station_2.calculate()
    assert isinstance(
        station_2.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)
