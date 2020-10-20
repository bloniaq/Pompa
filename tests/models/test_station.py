import pompa.models.station


def test_init():
    station = pompa.models.station.Station()
    assert station is not None
