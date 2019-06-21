import logging

log = logging.getLogger('pompa.view')


def set_shape(builder, ui_vars, shape):
        ui_vars.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = builder.get_object('Entry_Well_diameter')
        length = builder.get_object('Entry_Well_length')
        width = builder.get_object('Entry_Well_width')
        if shape == 'round':
            diameter.configure(state='normal')
            length.configure(state='disabled')
            width.configure(state='disabled')
        elif shape == 'rectangle':
            diameter.configure(state='disabled')
            length.configure(state='normal')
            width.configure(state='normal')
        log.debug('changed shape to {}'.format(shape))


def set_mode(builder, mode):
        """ Function sets some widgets properities, according to present work
        mode setting
        """

        nbook = builder.get_object('Notebook_Data')
        if mode == 'checking':
            nbook.tab(3, state='disabled')
            nbook.tab(4, state='disabled')
        elif mode == 'minimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='disabled')
        elif mode == 'optimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='normal')
        log.info('changed mode: {0}'.format(mode))


def set_wall_roughness(builder, wall_roughness):
    friction_reduct_entry = builder.get_object('Entry_Friction_reduction_coef')
    if wall_roughness == 'plain':
        friction_reduct_entry.configure(state='normal')
        return True
    elif wall_roughness == 'rough':
        friction_reduct_entry.configure(state='disabled')
        return True
    else:
        return False


def set_groundwater_inclusion(builder, inclusion):
    entries = [builder.get_object('Entry_Ord_groundwater'),
               builder.get_object('Entry_Solid_particles_vol_ratio'),
               builder.get_object('Entry_Solid_particles_density'),
               builder.get_object('Entry_Ground_fric_angle_dry'),
               builder.get_object('Entry_Ground_fric_angle_wet')]
    if inclusion:
        for e in entries:
            e.configure(state='normal')
    else:
        for e in entries:
            e.configure(state='disabled')
    return True
