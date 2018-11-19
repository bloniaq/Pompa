import logging

log = logging.getLogger('Pompa/main.classes')

default = {'mode': 'checking',
           'shape': 'round'}


def well_vars(object_):
    variables = {
        'well_diameter': [object_.diameter],
        'well_length': [object_.length],
        'well_width': [object_.width],
        'minimal_sewage_level': [object_.minimal_sewage_level],
        'ordinate_terrain': [object_.ord_terrain],
        'ordinate_inlet': [object_.ord_inlet],
        'ordinate_outlet': [object_.ord_outlet],
        'ordinate_bottom': [object_.ord_bottom],
        'ordinate_highest_point': [object_.ord_highest_point],
        'ordinate_final_table': [object_.ord_upper_level],
        'difference_in_start': [object_.difference_in_start],
        'inflow_max': [object_.inflow_max.value],
        'inflow_min': [object_.inflow_min.value]
    }
    return variables


def pump_vars(object_):
    variables = {
        '': [object_.diameter],
        'length_discharge_pipe': [object_.length],
        '': [object_.width],
        '': [object_.width]
    }
    return variables


def discharge_pipe_vars(object_):
    variables = {
        'length_discharge_pipe': [object_.length],
        'diameter_discharge_pipe': [object_.diameter],
        'roughness_discharge_pipe': [object_.roughness],
        'resistance_discharge_pipe': [object_.resistance_string]
    }
    return variables


def collector_vars(object_):
    variables = {
        'number_of_collectors': [object_.parallels],
        'length_collector': [object_.length],
        'roughness_collector': [object_.roughness],
        'resistance_collector': [object_.resistance_string],
        'diameter_collector': [object_.diameter]
    }
    return variables
