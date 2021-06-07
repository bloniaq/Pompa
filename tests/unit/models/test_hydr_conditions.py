import pompa.models.hydr_conditions as hydr_cond
import pompa.models.variables as v


def test_init():
    assert hydr_cond.HydrConditions() is not None

def test_geom_height():
    conditions = hydr_cond.HydrConditions()
    conditions.ord_upper_level.set(135.76)
    assert conditions.geom_height(122.51) == v.FloatVariable(13.25)
