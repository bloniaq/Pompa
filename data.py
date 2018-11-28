import logging
import classes as c

log = logging.getLogger('Pompa/main.data')

dan_mode = {'0': 'minimalisation', '1': 'checking', '2': 'optimalisation'}
dan_shape = {'0': 'rectangle', '1': 'round'}
dan_configuration = {'0': 'linear', '1': 'optimal'}
dan_reserve = {'1': 'minimal', '2': 'optimal', '3': 'safe'}


def well_vars(ins, app):
    ins.shape = c.Logic(app, 'rectangle', 'shape', '2', dan_shape,
                        app.ui_set_shape)
    ins.reserve_pumps = c.Logic(app, 'optimal', 'reserve_pumps', '4',
                                dan_reserve, None)
    ins.length = c.Numeric(app, 0.0, 'well_length', '6')
    ins.width = c.Numeric(app, 0.0, 'well_width', '7')
    ins.diameter = c.Numeric(app, 0.0, 'well_diameter', '8')
    ins.minimal_sewage_level = c.Numeric(app, 0.0, 'minimal_sewage_level', '9')
    ins.ord_terrain = c.Numeric(app, 0.0, 'ordinate_terrain', '10')
    ins.ord_outlet = c.Numeric(app, 0.0, 'ordinate_outlet', '11')
    ins.ord_inlet = c.Numeric(app, 0.0, 'ordinate_inlet', '12')
    ins.ord_bottom = c.Numeric(app, 0.0, 'ordinate_bottom', '13')
    ins.difference_in_start = c.Numeric(app, 0.0, 'difference_in_start', '14')
    ins.ord_highest_point = c.Numeric(app, 0.0, 'ordinate_highest_point', '15')
    ins.ord_upper_level = c.Numeric(app, 0.0, 'ordinate_final_table', '16')
    ins.inflow_min = c.Flow(app, 0.0, 'inflow_min', '33', 'inflow_unit')
    ins.inflow_max = c.Flow(app, 0.0, 'inflow_max', '34', 'inflow_unit')


def pump_vars(ins, app):
    ins.contour = c.Numeric(app, 0.0, 'pump_contour', '5')
    ins.cycle_time = c.Numeric(app, 0.0, 'work_cycle', '35')
    ins.efficiency_from = c.Flow(app, 0.0, 'pump_efficiency_from', '39',
                                 'pump_flow_unit')
    ins.efficiency_to = c.Flow(app, 0.0, 'pump_efficiency_to', '40',
                               'pump_flow_unit')
    ins.characteristic = c.PumpCharacteristic(app, 'Treeview_Pump',
                                              ['37', '38'])


def discharge_pipe_vars(ins, app):
    ins.length = c.Numeric(app, 0.0, 'length_discharge_pipe', '28')
    ins.diameter = c.Numeric(app, 0.0, 'diameter_discharge_pipe', '29')
    ins.roughness = c.Numeric(app, 0.0, 'roughness_discharge_pipe', '30')
    ins.resistance = c.Resistance(app, '', 'resistance_discharge_pipe', '32')


def collector_vars(ins, app):
    ins.parallels = c.Numeric(app, 0.0, 'number_of_collectors', '41', True)
    ins.length = c.Numeric(app, 0.0, 'length_collector', '42')
    ins.diameter = c.Numeric(app, 0.0, 'diameter_collector', '43')
    ins.roughness = c.Numeric(app, 0.0, 'roughness_collector', '44')
    ins.resistance = c.Resistance(app, '', 'resistance_collector', '47')
