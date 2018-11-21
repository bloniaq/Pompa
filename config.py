import logging

log = logging.getLogger('Pompa/main.classes')

default = {'mode': 'checking',
           'shape': 'round'}


def well_vars(object_):
    variables = {
        'well_diameter': ['diameter'],
        'well_length': ['length'],
        'well_width': ['width'],
        'minimal_sewage_level': ['minimal_sewage_level'],
        'ordinate_terrain': ['ord_terrain'],
        'ordinate_inlet': ['ord_inlet'],
        'ordinate_outlet': ['ord_outlet'],
        'ordinate_bottom': ['ord_bottom'],
        'ordinate_highest_point': ['ord_highest_point'],
        'ordinate_final_table': ['ord_upper_level'],
        'difference_in_start': ['difference_in_start'],
        'inflow_max': ['inflow_max.value'],
        'inflow_min': ['inflow_min.value']
    }
    return variables


def pump_vars(object_):
    variables = {
        '': ['diameter'],
        'length_discharge_pipe': ['length'],
        '': ['width'],
        '': ['width']
    }
    return variables


def discharge_pipe_vars(object_):
    variables = {
        'length_discharge_pipe': ['length'],
        'diameter_discharge_pipe': ['diameter'],
        'roughness_discharge_pipe': ['roughness'],
        'resistance_discharge_pipe': ['resistance.string']
    }
    return variables


def collector_vars(object_):
    variables = {
        'number_of_collectors': ['parallels'],
        'length_collector': ['length'],
        'roughness_collector': ['roughness'],
        'resistance_collector': ['resistance.string'],
        'diameter_collector': ['diameter']
    }
    return variables
