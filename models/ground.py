# libraries
import logging

# modules
import models.models as models
import models.variables as v

log = logging.getLogger('pompa.ground')


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

    def parameters(self, out_pipe, well, well_h):

        self.ground_vol_pipes = self.ground_volume_pipes(
            out_pipe.length.value, out_pipe.diameter.value,
            out_pipe.parallels.value)
        # self.ground_vol_well = self.ground_volume_well(well.)
        self.wall_thickness = 0.25
        self.plug_thickness = 1

        enough_density = False

        while not enough_density:
            log.debug('\n\nnext step')
            log.debug('wall_thickness: {}'.format(self.wall_thickness))
            log.debug('plug_thickness: {}'.format(self.plug_thickness))
            out_diameter = well.diameter.value + (2 * self.wall_thickness)
            self.wall_volume = self.calc_wall_vol(
                well.diameter.value, out_diameter, well_h)
            self.plug_volume = self.cylinder_vol(
                out_diameter, self.plug_thickness)
            self.well_weight = self.calc_well_weight(
                self.wall_volume, self.plug_volume)
            log.debug('well_weight: {}'.format(self.well_weight))

            self.lowering_friction = self.calc_friction_lowering(
                self.lateral_surface(out_diameter,
                                     well_h + self.plug_thickness))
            log.debug('lowering_friction: {}'.format(self.lowering_friction))
            if self.well_weight > self.lowering_friction:
                enough_density = True
            elif self.wall_thickness < 0.41:
                self.wall_thickness += 0.01
                continue
            else:
                self.plug_thickness += 0.1

        self.ground_vol_well = self.cylinder_vol(
            out_diameter, well_h + self.plug_thickness)
        return True

    def calc_well_weight(self, wall_vol, plug_vol):
        concrete_vol = wall_vol + plug_vol
        weight = self.concrete_density.value * concrete_vol
        return 9.81 * weight

    def calc_wall_vol(self, ins_d, out_d, well_h):
        log.debug('ins: d: {}, well_h: {}'.format(ins_d, well_h))
        vol_ins = self.cylinder_vol(ins_d, well_h)
        vol_out = self.cylinder_vol(out_d, well_h)
        return vol_out - vol_ins

    def lateral_surface(self, out_diameter, out_height):
        lateral_surface = 3.14 * out_diameter * out_height
        return lateral_surface

    def calc_friction_lowering(self, area):
        friction = self.ground_friction.value * area
        return friction

    def ground_volume_pipes(self, p_length, p_diameter, p_number):
        excav_height = (p_diameter * 0.001) + 1
        excav_length = p_length
        if p_number == 1 and p_diameter <= 500:
            excav_width = (p_diameter * 0.001) + 0.8
        else:
            excav_width = (p_diameter * 0.001) + 1.2
        volume = excav_height * excav_width * excav_length
        return volume

    def ground_volume_well(self, excav_height, area):
        volume = area * excav_height
        return volume

    def cylinder_vol(self, diameter, height):
        volume = 3.14 * ((diameter / 2) ** 2) * height
        return volume
