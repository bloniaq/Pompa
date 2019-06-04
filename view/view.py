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
