import logging
import models.variables as v

log = logging.getLogger('pompa.data')

dan_mode = {'0': 'minimalisation', '1': 'checking', '2': 'optimalisation'}
dan_shape = {'0': 'rectangle', '1': 'round'}
dan_configuration = {'0': 'singlerow', '1': 'optimal'}
dan_reserve = {'1': 'minimal', '2': 'optimal', '3': 'safe'}
dan_walls = {'0': 'rough', '1': 'plain'}
dan_gndwater = {'0': 0, '1': 1}

default = {'mode': 'checking',
           'shape': 'round'}

# HOW TO GET WIDGET BY TK VAR?
# Another comment just for tests (git)


def station_vars(app):
    ins = app.station

    ins.reserve_pumps = v.Logic(app, 'optimal', 'reserve_pumps', '4',
                                dan_reserve, None)
    ins.minimal_sewage_level = v.P_Float(app, 0.0, 'minimal_sewage_level', '9')
    ins.ord_terrain = v.P_Float(app, 0.0, 'ordinate_terrain', '10')
    ins.ord_outlet = v.P_Float(app, 0.0, 'ordinate_outlet', '11')
    ins.ord_inlet = v.P_Float(app, 0.0, 'ordinate_inlet', '12',
                              fig_depend="schema")
    ins.ord_bottom = v.P_Float(app, 0.0, 'ordinate_bottom', '13')
    ins.difference_in_start = v.P_Float(app, 0.0, 'difference_in_start', '14')
    ins.ord_highest_point = v.P_Float(app, 0.0, 'ordinate_highest_point', '15')
    ins.ord_upper_level = v.P_Float(app, 0.0, 'ordinate_final_table', '16',
                                    fig_depend="schema")
    ins.inflow_min = v.Flow(app, 0.0, 'inflow_min', '33', 'inflow_unit',
                            fig_depend="pump_char")
    ins.inflow_max = v.Flow(app, 0.0, 'inflow_max', '34', 'inflow_unit',
                            fig_depend="pump_char")


def well_vars(app):
    ins = app.station.well

    ins.shape = v.Logic(app, 'rectangle', 'shape', '2', dan_shape,
                        app.ui_set_shape)
    ins.config = v.Logic(app, 'singlerow', 'pump_configuration', '3',
                         dan_configuration, None)
    ins.length = v.P_Float(app, 0.0, 'well_length', '6')
    ins.width = v.P_Float(app, 0.0, 'well_width', '7')
    ins.diameter = v.P_Float(app, 0.0, 'well_diameter', '8')


def pump_vars(app):
    ins = app.station.pump

    ins.contour = v.P_Float(app, 0.0, 'pump_contour', '5')
    ins.cycle_time = v.P_Float(app, 0.0, 'work_cycle', '35')
    ins.efficiency_from = v.Flow(app, 0.0, 'pump_efficiency_from', '39',
                                 'pump_flow_unit', fig_depend="pump_char")
    ins.efficiency_to = v.Flow(app, 0.0, 'pump_efficiency_to', '40',
                               'pump_flow_unit', fig_depend="pump_char")
    ins.characteristic = v.PumpCharacteristic(app, 'Treeview_Pump',
                                              ['37', '38'], 'pump_flow_unit')


def ins_pipe_vars(app):
    ins = app.station.ins_pipe

    ins.length = v.P_Float(app, 0.0, 'length_discharge_pipe', '28',
                           fig_depend="pipe_char")
    ins.diameter = v.P_Float(app, 0.0, 'diameter_discharge_pipe', '29',
                             fig_depend="pipe_char")
    ins.roughness = v.P_Float(app, 0.0, 'roughness_discharge_pipe', '30',
                              fig_depend="pipe_char")
    ins.resistance = v.Resistance(app, '', 'resistance_discharge_pipe', '32')
    ins.l_res_coef = 0.6


def out_pipe_vars(app):
    ins = app.station.out_pipe

    ins.parallels = v.P_Int(app, 0, 'number_of_collectors', '41')
    ins.length = v.P_Float(app, 0.0, 'length_collector', '42',
                           fig_depend="pipe_char")
    ins.diameter = v.P_Float(app, 0.0, 'diameter_collector', '43',
                             fig_depend="pipe_char")
    ins.roughness = v.P_Float(app, 0.0, 'roughness_collector', '44',
                              fig_depend="pipe_char")
    ins.resistance = v.Resistance(app, '', 'resistance_collector', '47')


def get_data_dict_from_dan_file(path, filename):
    log.info('\ndan_load started\n')
    log.info('plik danych generowany wersją 1.0 aplikacji')
    data_dictionary = {}

    with open(path, 'r+') as file:
        log.info('opening file: {0}\n\n'.format(str(file)))
        for line in file:
            try:
                id_line, line_datas = line.split(')')
            except ValueError as e:
                log.error('ValueError {}'.format(e))
            line_datas_list = line_datas.split()
            stored_value = line_datas_list[0]
            log.debug('id: {}, stored value: {}'.format(
                id_line, stored_value))
            if id_line not in data_dictionary:
                data_dictionary[id_line] = []
            data_dictionary[id_line].append(stored_value)
            log.debug('dan_id: {}, value: {}'.format(
                id_line, data_dictionary[id_line]))
        log.debug('dictionary in progress: {}'.format(data_dictionary))
        for id_ in data_dictionary:
            if len(data_dictionary[id_]) == 1:
                data_dictionary[id_] = data_dictionary[id_][0]
                data_dictionary[id_] = float(data_dictionary[id_])
                # expand for exceptions, make floats
            else:
                data_dictionary[id_] = [float(s)
                                        for s in data_dictionary[id_]]
        log.debug('dictionary at finish: {}'.format(data_dictionary))
        return data_dictionary
