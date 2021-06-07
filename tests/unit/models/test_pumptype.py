import pompa.models.pumptype as pumptype


def test_init():
    pump_type = pumptype.PumpType()
    assert pump_type is not None


def test_attributes_types():
    pump_type = pumptype.PumpType()
    assert isinstance(pump_type.cycle_time, pumptype.v.IntVariable)
    assert isinstance(pump_type.contour, pumptype.v.FloatVariable)
    assert isinstance(pump_type.suction_level, pumptype.v.FloatVariable)
    assert isinstance(pump_type.efficiency_from, pumptype.v.FlowVariable)
    assert isinstance(pump_type.efficiency_to, pumptype.v.FlowVariable)
    assert isinstance(pump_type.characteristic, pumptype.v.PumpCharVariable)

def test_optimal_range():
    pump_type = pumptype.PumpType()
    pump_type.efficiency_from.set(15, 'lps')
    pump_type.efficiency_to.set(20, 'lps')
    assert pump_type.opt_range(2)[0].value_lps == 30
    assert pump_type.opt_range(2)[1].value_lps == 40