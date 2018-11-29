import logging

log = logging.getLogger('Pompa/main.hydraulics')


def pipe_loss(app, flow):
    result = app.well.height_to_pump() + app.discharge_pipe.sum_loss(flow) + \
        app.collector.sum_loss(flow)
    log.info('pipes loss: {}'.format(result))
    return result
