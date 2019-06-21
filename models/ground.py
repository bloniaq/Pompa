# libraries
import logging

# modules
import models.models as models
import models.variables as v

log = logging.getLogger('pompa.station')


class Ground(models.StationObject):

    def __init__(self, app):
        super().__init__(app)

    # input parameters

        self.concrete_density = None
        self.ground_friction = None
        self.is_walls_plain = None
        self.friction_reduction_coef = None
        self.include_groundwater = None
        self.ord_groundwater = None
        self.solid_particles_vol_ratio = None
        self.solid_particles_density = None
        self.ground_fric_angle_dry = None
        self.ground_fric_angle_wet = None
        self.wall_ground_fric_coef = None

        # calculate parameters

        self.ground_vol_pipes = 0
        self.ground_vol_well = 0
        self.wall_thickness = 0
        self.wall_volume = 0
        self.plug_thickness = 0
        self.plug_volume = 0
        self.lowering_friction = 0
        self.buoyancy = 0
        self.well_weight = 0

    def calculations():

        pass
