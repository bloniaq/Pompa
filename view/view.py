import logging

log = logging.getLogger('pompa.view')


def set_shape(builder, ui_vars, shape, mode):
        ui_vars.__getitem__('shape').set(shape)
        log.debug('started setting shape')
        log.debug('new shape: {}'.format(shape))
        diameter = builder.get_object('Entry_Well_diameter')
        length = builder.get_object('Entry_Well_length')
        width = builder.get_object('Entry_Well_width')
        if mode == 'checking':
            if shape == 'round':
                diameter.configure(state='normal')
                length.configure(state='disabled')
                width.configure(state='disabled')
            elif shape == 'rectangle':
                diameter.configure(state='disabled')
                length.configure(state='normal')
                width.configure(state='normal')
        else:
            diameter.configure(state='disabled')
            length.configure(state='disabled')
            width.configure(state='disabled')
        log.debug('changed shape to {}'.format(shape))


def set_mode(builder, ui_vars, mode):
        """ Function sets some widgets properities, according to present work
        mode setting
        """

        nbook = builder.get_object('Notebook_Data')
        ord_bottom_label = ui_vars.__getitem__('ord_bottom_label')
        if mode == 'checking':
            nbook.tab(3, state='disabled')
            nbook.tab(4, state='disabled')
            ord_bottom_label.set('Rzędna dna pompowni [m]')
        elif mode == 'minimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='disabled')
            ord_bottom_label.set('Rzędna dna pompowni (założenie) [m]')
        elif mode == 'optimalisation':
            nbook.tab(3, state='normal')
            nbook.tab(4, state='normal')
            ord_bottom_label.set('Rzędna dna pompowni (założenie) [m]')
        log.info('changed mode: {0}'.format(mode))


def set_wall_roughness(builder, wall_roughness):
    friction_reduct_entry = builder.get_object('Entry_Friction_reduction_coef')
    if wall_roughness == 'plain':
        friction_reduct_entry.configure(state='normal')
        log.info('changed wall_roughness: {}'.format(wall_roughness))
        return True
    elif wall_roughness == 'rough':
        friction_reduct_entry.configure(state='disabled')
        log.info('changed wall_roughness: {}'.format(wall_roughness))
        return True
    else:
        log.error('Wrong wall_roughness value: {}'.format(wall_roughness))
        return False


def set_groundwater_inclusion(builder, inclusion):
    entries = [builder.get_object('Entry_Ord_groundwater'),
               builder.get_object('Entry_Solid_particles_vol_ratio'),
               builder.get_object('Entry_Solid_particles_density'),
               builder.get_object('Entry_Ground_fric_angle_dry'),
               builder.get_object('Entry_Ground_fric_angle_wet'),
               builder.get_object('Entry_Avg_fric_coef')]
    if inclusion:
        for e in entries:
            e.configure(state='normal')
    else:
        for e in entries:
            e.configure(state='disabled')
    return True
