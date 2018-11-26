import logging

log = logging.getLogger('Pompa/main.classes')

default = {'mode': 'checking',
           'shape': 'round'}

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}
dan_mode = {'0': 'minimalisation', '1': 'checking', '2': 'optimalisation'}
dan_shape = {'0': 'rectangle', '1': 'round'}
dan_configuration = {'0': 'linear', '1': 'optimal'}
dan_reserve = {'1': 'minimal', '2': 'optimal', '3': 'safe'}
dan_dicts = [
    dan_mode,
    dan_shape,
    dan_configuration,
    dan_reserve
]

load_dictionary = {
    '1': ['mode', 'dan_dicts'],
    '2': ['shape', 'dan_dicts'],
    '3': ['pump_configuration', 'dan_dicts'],
    '4': ['reserve_pumps', 'dan_dicts'],
    '5': ['pump_contour', 'float'],
    '6': ['well_length', 'float'],
    '7': ['well_width', 'float'],
    '8': ['well_diameter', 'float'],
    '9': ['minimal_sewage_level', 'float'],
    '10': ['ordinate_terrain', 'float'],
    '11': ['ordinate_outlet', 'float'],
    '12': ['ordinate_inlet', 'float'],
    '13': ['ordinate_bottom', 'float'],
    '14': ['difference_in_start', 'float'],
    '15': ['ordinate_highest_point', 'float'],
    '16': ['ordinate_final_table', 'float'],
    '28': ['length_discharge_pipe', 'float'],
    '29': ['diameter_discharge_pipe', 'float'],
    '30': ['roughness_discharge_pipe', 'float'],
    '32': ['resistance_discharge_pipe', 'list'],
    '33': ['inflow_min', 'float'],
    '34': ['inflow_max', 'float'],
    '35': ['work_cycle', 'float'],
    '37': ['pump_flow_coords', 'pump'],
    '38': ['pump_lift_coords', 'pump'],
    '39': ['pump_efficiency_from', 'float'],
    '40': ['pump_efficiency_to', 'float'],
    '41': ['number_of_collectors', 'int'],
    '42': ['length_collector', 'float'],
    '43': ['diameter_collector', 'float'],
    '44': ['roughness_collector', 'float'],
    '46': ['resistance_collector', 'list']
}


def prepare_value(input_id, input_data):
    log.debug('input data: {}, {}'.format(input_data, type(input_data)))
    if input_id not in load_dictionary:
        return ''
    method = load_dictionary[input_id][1]
    if method == 'dan_dicts':
        output = dan_dicts[int(input_id) - 1][input_data[0]]
    elif method == 'float':
        output = float(input_data[0])
    elif method == 'int':
        output = int(input_data[0])
    elif method == 'list':
        output = str(input_data[0])
        if len(input_data) > 1:
            for element in range(1, len(input_data)):
                output += ', {}'.format(str(element))
    elif method == 'pump':
        output = [float(val) for val in input_data]
    log.debug('output data: {}, {}'.format(output, type(output)))
    return output


def well_vars():
    variables = {
        'shape': ['shape', '2'],
        'well_diameter': ['diameter', '8'],
        'well_length': ['length', '6'],
        'well_width': ['width', '7'],
        'minimal_sewage_level': ['minimal_sewage_level', '9'],
        'ordinate_terrain': ['ord_terrain', '10'],
        'ordinate_inlet': ['ord_inlet', '12'],
        'ordinate_outlet': ['ord_outlet', '11'],
        'ordinate_bottom': ['ord_bottom', '13'],
        'ordinate_highest_point': ['ord_highest_point', '15'],
        'ordinate_final_table': ['ord_upper_level', '16'],
        'difference_in_start': ['difference_in_start', '14'],
        'inflow_max': ['inflow_max.value', '34'],
        'inflow_min': ['inflow_min.value', '33']
    }
    return variables


def pump_vars():
    variables = {
        'work_cycle': ['cycle_time', '35'],
        # '': ['suction_level'],
        'pump_contour': ['contour', '5'],
        'pump_flow_coords': ['pump_flow_coords', '37'],
        'pump_lift_coords': ['pump_lift_coords', '38'],
        'pump_efficiency_from': ['efficiency_from.value', '39'],
        'pump_efficiency_to': ['efficiency_to.value', '40']
    }
    return variables


def discharge_pipe_vars():
    variables = {
        'length_discharge_pipe': ['length', '28'],
        'diameter_discharge_pipe': ['diameter', '29'],
        'roughness_discharge_pipe': ['roughness', '30'],
        'resistance_discharge_pipe': ['resistance.string', '32']
    }
    return variables


def collector_vars():
    variables = {
        'number_of_collectors': ['parallels', '41'],
        'length_collector': ['length', '42'],
        'roughness_collector': ['roughness', '44'],
        'resistance_collector': ['resistance.string', '46'],
        'diameter_collector': ['diameter', '43']
    }
    return variables
