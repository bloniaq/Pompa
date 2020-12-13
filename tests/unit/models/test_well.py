import pytest
import pompa.models.well


def test_init():
    well = pompa.models.well.Well()
    assert well is not None


@pytest.mark.parametrize("config, netto_contour, pump_n, result", [
    ("singlerow", 1, 2, 2.6),
    ("singlerow", 2, 8, 18.4),
    ("optimal", 1.1, 4, 3.39),
    ("optimal", 0.4, 15, 3.16)])
def test_min_diameter(config, netto_contour, pump_n, result):
    well = pompa.models.well.Well()
    well.config = config
    assert well.minimal_diameter(pump_n, netto_contour) == result
