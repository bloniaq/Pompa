import logging
import maths

log = logging.getLogger('Pompa.hydraulics')


def pipes_ready(app):
    log.debug('Are pipes ready?')
    flag = True
    if not app.discharge_pipe.pipe_char_ready():
        flag = False
    log.debug(flag)
    if not app.collector.pipe_char_ready():
        flag = False
    log.debug(flag)
    return flag


def pipe_loss(app, flow):
    result = app.well.height_to_pump() + app.discharge_pipe.sum_loss(flow) + \
        app.collector.sum_loss(flow)
    log.info('pipes loss: {}'.format(result))
    return result


def draw_pipes_plot(app, x_lin, unit):
    log.debug('Starting draw_pipes_plot')
    flows, _ = app.pump.characteristic.get_pump_char_func()
    geom_loss = app.well.height_to_pump()
    discharge_y = app.discharge_pipe.get_y_coords(flows, unit)
    collector_y = app.collector.get_y_coords(flows, unit)
    pipes_char = []
    for i in range(len(flows)):
        pipes_char.append(geom_loss + discharge_y[i] + collector_y[i])
    y = maths.fit_coords(flows, pipes_char, 1)
    return x_lin, y(x_lin), 'g-'


def number_of_pumps(app):
    return 4
