import pompa.models.pumpset
from pompa.models.pumptype import PumpType
import pompa.models.variables as v


def test_init_existance(station_1):
    assert pompa.models.pumpset.PumpSet(
        station_1.pump_type, 0.00, 1, station_1.hydr_cond.inflow_min,
        station_1.hydr_cond.inflow_max) is not None


def test_init_pumptype_attribute(station_1, pumpsystem_for_station_1):
    pumpsystem = pumpsystem_for_station_1
    stop_ord = pumpsystem._stop_ordinate(station_1.hydr_cond.ord_bottom)
    w_pump_amount = 1
    inflow_min = station_1.hydr_cond.inflow_min
    inflow_max = station_1.hydr_cond.inflow_max
    pumpset = pompa.models.pumpset.PumpSet(
        station_1.pump_type, stop_ord, w_pump_amount, inflow_min, inflow_max)
    assert isinstance(pumpset.pump_type, PumpType)
    assert isinstance(pumpset.stop_ord, v.FloatVariable)
