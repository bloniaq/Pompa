# libraries
import logging

# modules
import models.models as models

log = logging.getLogger('pompa.economy')


class Economy(models.StationObject):

    def __init__(self, app):
        super().__init__(app)

        # input parameters
        self.optimalisation_time = None  # years
        self.price_energy = None  # kW/h
        self.employees = None
        self.salary = None  # zł
        self.failure_free_work = None  # hours
        self.repairs_no = None
        self.price_pump = None
        self.repair_cost = None
        self.price_close_valve = None
        self.price_flap_valve = None
        self.price_pipe = None
        self.price_terrain = None
        self.price_concrete = None
        self.price_labor_eq = None  # percent of material
        self.price_extraction = None
        self.building_time = None  # days
        self.characteristic = None
        self.wells_no = None
        self.well_bottom = None
        self.price_well = None
        self.aggr_efficiency = None
        self.daily_inflow = None
        self.yearly_inflow_irreg = None
        self.pump_efficiency = None
        self.engine_efficiency = None

        # calculate parameters
