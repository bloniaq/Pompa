import logging

log = logging.getLogger('Pompa/main.hydraulics')


def are_pipes_defined(app):
    flag = True
    checklist = [app.discharge_pipe.length,
                 app.discharge_pipe.diameter,
                 app.discharge_pipe.roughness,
                 app.collector.length,
                 app.collector.diameter,
                 app.collector.roughness
                 ]
    for element in checklist:
        if element.value == 0:
            flag = False
            log.debug('this parameter is undefined: {}'.format(element))
    log.debug('is pipes defined: {}'.format(flag))
    return flag


def pipe_loss(app, flow):
    result = app.well.height_to_pump() + app.discharge_pipe.sum_loss(flow) + \
        app.collector.sum_loss(flow)
    log.info('pipes loss: {}'.format(result))
    return result
