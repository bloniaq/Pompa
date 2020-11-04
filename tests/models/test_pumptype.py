import pompa.models.pumptype as pumptype


def test_init():
    pump_type = pumptype.Pump_Type()
    assert pump_type is not None


def test_attributes_types():
    pump_type = pumptype.Pump_Type()
    assert isinstance(pump_type.cycle_time, pumptype.v.IntVariable)
    assert isinstance(pump_type.contour, pumptype.v.FloatVariable)
    assert isinstance(pump_type.suction_level, pumptype.v.FloatVariable)
    assert isinstance(pump_type.efficiency_from, pumptype.v.FlowVariable)
    assert isinstance(pump_type.efficiency_to, pumptype.v.FlowVariable)
    assert isinstance(pump_type.characteristic, pumptype.v.PumpCharVariable)


def test_max_efficiency():
    pump_type = pumptype.Pump_Type()
    pump_type.efficiency_from.set(15)
    pump_type.efficiency_to.set(25)
    expected_efficiency = pumptype.v.FlowVariable(20)
    assert pump_type.max_efficiency() == expected_efficiency
