# libraries
import logging

# modules
import models.models as models

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

    """
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
            self.well_weight = self.well_f_grav(
                self.wall_volume, self.plug_volume)
            log.debug('well_f_grav: {}'.format(self.well_weight))

            self.lowering_friction = self.calc_friction_lowering(
                self.lateral_surface(out_diameter,
                                     well_h + self.plug_thickness))
            log.debug('lowering_friction: {}'.format(self.lowering_friction))
            if self.well_weight > self.lowering_friction:
                enough_density = True
            elif self.wall_thickness < 0.61:
                self.wall_thickness += 0.01
                continue
            else:
                self.plug_thickness += 0.1

        self.ground_vol_well = self.cylinder_vol(
            out_diameter, well_h + self.plug_thickness)
        return True
    """

    def parameters(self, ord_bottom, ins_d, ins_h):
        ''' Okrojona wersja funkcji

        Jeśli liczymy wypór, to od niego zaczynamy, bo musimy wiedzieć jak
        grubego korka potrzebujemy - a to wpływa na wysokość zewn studni.
        Liczenie korka polega na iterowaniu jego grubości aż ciężar jego,
        jak i samej studni oraz siła tarcia, łącznie przeważą siłę wyporu

        Potem spradzamy czy ciężar bez korka przeważa tarcie,
        dla znanej już wysokości studni
        Nadal nie wiem jaka powinna być powierzchnia tarcia

        Następnie obliczamy objętość robót ziemnych

        '''
        '''
        plug_th = 1
        wall_th = 0.25

        if self.include_groundwater.value:
            buoyancy_overcome = False
            out_d = ins_d + 2 * wall_th
            wall_vol_over_plug = self.cylinder_volume(
                ins_h, out_d) - self.cylinder_volume(ins_h, ins_d)
            while not buoyancy_overcome:
                # iterate over plug thickness until it overcome buoyancy
                ord_plug_bottom = ord_bottom - plug_th
                buoyancy = self.calc_buoyancy(ord_plug_bottom, out_d)
                f_grav_wout_plug = self.f_grav(self.concrete_density.value,
                                               wall_vol_over_plug)
                f_grav_plug = self.f_grav(self.concrete_density.value,
                                          self.cylinder_volume(plug_th, ins_d))
                # f_frict = 
                f_stab = f_grav_wout_plug + f_grav_plug + f_frict
                if True:  # buoyancy < f_stab:
                    buoyancy_overcome = True
                elif self.wall_thickness < 0.41:
                    self.wall_thickness += 0.01
                    continue
                else:
                    plug_th = self.adjust_plug_th()
        return True
        '''
        pass

    def calc_buoyancy(self, ord_plug_bottom, diameter):
        ''' Returns buoyancy value
        '''
        volume = self.cylinder_volume(self.ord_groundwater - ord_plug_bottom,
                                      diameter)
        water_density = 1000  # kg/m3
        return volume * water_density * 9.81

    def f_grav(self, density, *volume):
        ''' Returns value of gravity force acting on empty well
        Args have to be in m3 unit. Conrete density is kN/m3. Result is kN.
        '''
        return 9.81 * density * sum(volume)

    def f_frict(self, area, coef):
        f_friction = area * coef * 9.81
        return f_friction

    def cylinder_volume(self, height, diameter):
        return 3.14 * 0.25 * (diameter ** 2) * height

    def calc_wall_vol(self, ins_d, out_d, well_h):
        log.debug('ins: d: {}, well_h: {}'.format(ins_d, well_h))
        vol_ins = self.cylinder_vol(ins_d, well_h)
        vol_out = self.cylinder_vol(out_d, well_h)
        return vol_out - vol_ins

    def lateral_surface(self, out_diameter, out_height):
        lateral_surface = 3.14 * out_diameter * out_height
        return lateral_surface

    def calc_friction_lowering(self, fric_area):
        friction = self.ground_friction.value * 9.81 * fric_area
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
