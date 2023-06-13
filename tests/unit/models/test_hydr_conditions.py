import pompa.models.hydr_conditions as hydr_cond
import pompa.models.variables as v


def test_init():
    assert hydr_cond.HydrConditions() is not None

def test_geom_height():
    conditions = hydr_cond.HydrConditions()
    conditions.ord_upper_level.set(135.76)
    ordinate_to_check = v.FloatVariable(122.51)
    assert conditions.geom_height(ordinate_to_check) == v.FloatVariable(13.25)

def test_max_pump_start_ord():
    conditions = hydr_cond.HydrConditions()
    conditions.ord_inlet.set(10.22)
    conditions.reserve_height.set(.11)
    ordinate_to_check = v.FloatVariable(10.11)
    assert conditions.max_pump_start_ord() == ordinate_to_check
