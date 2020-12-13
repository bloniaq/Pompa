import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None


def test_calculation_run():
    station = pompa.models.station.Station()
    station.calculate()
    assert isinstance(
        station.pumpsystem, pompa.models.station.pumpsystem.PumpSystem)
