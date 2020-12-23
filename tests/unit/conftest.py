import pytest
import pompa.models.workpoint
import pompa.models.variables as v
import numpy as np
from pompa.models.station import Station
from pompa.models.pumpsystem import PumpSystem


@pytest.fixture
def station_1(request):
    station = Station()

    # Pump Type
    station.pump_type.suction_level.set(0.3)
    station.pump_type.efficiency_from.set(23.5, 'lps')
    station.pump_type.efficiency_to.set(37, 'lps')

    # Hydraulic Conditions
    station.hydr_cond.ord_bottom.set(138.57)
    station.hydr_cond.inflow_min.set(11, 'lps')
    station.hydr_cond.inflow_max.set(22, 'lps')

    # Inside Pipe
    station.ins_pipe.length.set(7)
    station.ins_pipe.diameter.set(.150)
    station.ins_pipe.roughness.set(.0008)
    station.ins_pipe.resistance.set([0.27, 0.27, 0.6, 0.2, 2, 0.04])
    station.ins_pipe.parallels.set(1)

    # Outside Pipe
    station.out_pipe.length.set(732)
    station.out_pipe.diameter.set(.200)
    station.out_pipe.roughness.set(0.0005)
    station.out_pipe.resistance.set([])
    station.out_pipe.parallels.set(1)
    return station


@pytest.fixture
def pumpsystem_for_station_1(station_1):
    s = station_1
    return PumpSystem(s.well, s.ins_pipe, s.out_pipe, s.pump_type, s.hydr_cond)
