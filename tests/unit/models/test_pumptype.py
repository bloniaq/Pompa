import pompa.models.pumptype as pumptype
import pompa.models.variables as v
import pytest


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
    v.Variable.clean_registry()
    assert pump_type.opt_range(2)[1].value_lps == 40

def test_shutdown_ord():
    pump_type = pumptype.PumpType()
    pump_type.suction_level.set(0.35)
    assert pump_type.shutdown_ord(v.FloatVariable(95.65)) == v.FloatVariable(
        96)

@pytest.fixture
def ptype_proper():
    pump = pumptype.PumpType()
    pump.efficiency_to.set(25, 'lps')
    pump.efficiency_from.set(20, 'lps')
    pump.contour.set(0.30)
    pump.cycle_time.set(3)
    pump.suction_level.set(0.50)
    pump.characteristic.add_point(20, 14)
    pump.characteristic.add_point(21, 13.5)
    pump.characteristic.add_point(22, 12.8)
    pump.characteristic.add_point(23, 12)
    pump.characteristic.add_point(24, 11.3)
    return pump

def test_validate_all_good(ptype_proper):
    assert ptype_proper.validate()

def test_validate_4_points(ptype_proper):
    point = ptype_proper.characteristic.value[1]
    ptype_proper.characteristic.remove_point(point)
    assert not ptype_proper.validate()

def test_validate_wrong_eff(ptype_proper):
    ptype_proper.efficiency_to.set(18, 'lps')
    assert not ptype_proper.validate()

def test_validate_contour(ptype_proper):
    ptype_proper.contour.set(-18)
    assert not ptype_proper.validate()

def test_validate_cycle_time(ptype_proper):
    ptype_proper.cycle_time.set(-18)
    assert not ptype_proper.validate()

def test_validate_suction_lvl(ptype_proper):
    ptype_proper.suction_level.set(-18)
    assert not ptype_proper.validate()
