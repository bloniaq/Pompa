import logging

log = logging.getLogger('Pompa/main.classes')

default = {'mode': 'checking',
           'shape': 'round'}


def well_vars(object_):
    ref_dict = object_.__dict__
    variables = {
        'well_diameter': [object_.__dict__['diameter']],
        'well_length': [ref_dict['length']],
        'well_width': [ref_dict['width']],
        'minimal_sewage_level': [ref_dict['minimal_sewage_level']],
        'ordinate_terrain': [ref_dict['ord_terrain']],
        'ordinate_inlet': [ref_dict['ord_inlet']],
        'ordinate_outlet': [ref_dict['ord_outlet']],
        'ordinate_bottom': [ref_dict['ord_bottom']],
        'ordinate_highest_point': [ref_dict['ord_highest_point']],
        'ordinate_final_table': [ref_dict['ord_upper_level']],
        'difference_in_start': [ref_dict['difference_in_start']],
        'inflow_max': [ref_dict['inflow_max'].value],
        'inflow_min': [ref_dict['inflow_min'].value]
    }
    return variables


def pump_vars(object_):
    ref_dict = object_.__dict__
    variables = {
        '': [['diameter']],
        'length_discharge_pipe': [ref_dict['length']],
        '': [ref_dict['width']],
        '': [ref_dict['width']]
    }
    return variables


def discharge_pipe_vars(object_):
    ref_dict = object_.__dict__
    variables = {
        'length_discharge_pipe': [ref_dict['length']],
        'diameter_discharge_pipe': [ref_dict['diameter']],
        'roughness_discharge_pipe': [ref_dict['roughness']],
        'resistance_discharge_pipe': [ref_dict['resistance_string']]
    }
    return variables


def collector_vars(object_):
    ref_dict = object_.__dict__
    variables = {
        'number_of_collectors': [ref_dict['parallels']],
        'length_collector': [ref_dict['length']],
        'roughness_collector': [ref_dict['roughness']],
        'resistance_collector': [ref_dict['resistance_string']],
        'diameter_collector': [ref_dict['diameter']]
    }
    return variables
