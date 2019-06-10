import logging
import numpy as np

log = logging.getLogger('Pompa.calcs')

unit_bracket_dict = {'liters': '[l/s]', 'meters': '[m³/h]'}


def work_point(pump, pipes):
    return np.argwhere(np.diff(np.sign(pump - pipes))).flatten()


def interp(wanted_x, x_arr, y_arr):
    return np.interp(wanted_x, x_arr, y_arr)


def fit_coords(xcoords, ycoords, degree):
    log.debug('x: {}, y:{}'.format(xcoords, ycoords))
    x, y = sort_by_x(xcoords, ycoords)
    log.debug('arr x: {}, arr y:{}'.format(x, y))
    polyf = np.polyfit(x, y, degree)
    fitted_y = np.poly1d(polyf)
    log.debug('arr x: {}, fit y:{}'.format(x, fitted_y))
    return fitted_y


def sort_by_x(x_list, y_list):
        xcoords = []
        ycoords = []
        pairs = {}
        for i in range(len(x_list)):
            pairs[str(x_list[i])] = y_list[i]
            xcoords.append(x_list[i])
        xcoords.sort()
        for value in xcoords:
            ycoords.append(pairs[str(value)])
        x = np.array(xcoords)
        y = np.array(ycoords)
        return x, y


def calc_number_of_pumps(station):
    """Sets number of work pumps, based on min and max inflow, and pump
    efficiency

    TO MAKE TEST THIS FUNCTION!
    """
    log.debug('calc_number_of_pumps START')
    max_pump_eff = station.pump.max_pump_efficiency()
    log.debug('minimal inflow value_liters {}'.format(
        station.inflow_min.value_liters))
    if max_pump_eff.value_liters < station.inflow_min.value_liters:
        log.error('Too low pump efficiency !!!')
        ##############################
        # EXCEPTION TO RAISE !!!
        ##############################
        log.error('Pump has too less efficiency to this station')
        return 0
    number_of_pumps = int(np.ceil((1.1 * station.inflow_max.value_liters) /
                                  max_pump_eff.value_liters))
    log.debug('Result: {}'.format(number_of_pumps))
    station.number_of_pumps = number_of_pumps
    return number_of_pumps


def reserve_pumps_number(station):
    """Sets number of reserve pumps, based on user choose"""
    if station.reserve_pumps.value == 'minimal':
        n_of_res_pumps = 1
    elif station.reserve_pumps.value == 'optimal':
        if station.number_of_pumps % 2 == 0:
            n_of_res_pumps = int(station.number_of_pumps / 2)
        else:
            n_of_res_pumps = int(station.number_of_pumps / 2) + 1
    elif station.reserve_pumps.value == 'safe':
        n_of_res_pumps = station.number_of_pumps
    station.number_of_res_pumps = n_of_res_pumps
    return n_of_res_pumps


def check_get_useful_velo(station):
    useful_velo = ((((
        station.pump.cycle_time.value) * 60) * station.qp) / 4000)
    log.info('useful velo is {}m3'.format(useful_velo))
    return useful_velo


def get_work_parameters(station, flow, start_ord):
        """ Returns tuple of work parameters:
        (LC highness, geometric highness, flow, speed in collector,
         speed in discharge)
        """
        start_ordi = station.ord_bottom.value + station.minimal_sewage_level.value
        geom_H = station.ord_upper_level.value - start_ordi
        # flow = flow.value_liters  # l/s
        difference = 100
        step = 0.05
        pump_x = self.get_x_axis('liters')
        flows, lifts = station.pump.characteristic.get_pump_char_func(
            "liters")
        pump_y = maths.fit_coords(flows, lifts, 3)(pump_x)
        log.debug("pump x: {} len {}, pump y: {} len {}".format(
            pump_x, len(pump_x), pump_y, len(pump_y)))
        log.debug('WE\'RE IN LOOP')
        while True:
            log.debug('LOOP WHILE')
            log.debug('Flow : {}'.format(flow))
            pipe_val = geom_H + self.d_pipe.sum_loss(
                flow, "liters") + self.collector.sum_loss(flow, "liters")
            pump_val = maths.interp(flow, pump_x, pump_y)
            log.debug('pipe_val : {}'.format(pipe_val))
            log.debug('pump_val : {}'.format(pump_val))
            difference = pump_val - pipe_val
            if difference < -0.1:
                log.debug('difference < 0.1: {}'.format(difference))
                flow = flow - step
            elif difference > 0.1:
                log.debug('difference > 0.1: {}'.format(difference))
                flow = flow + step
            else:
                break
        speed_coll = (flow * 0.001) / self.collector.get_area()
        speed_dpipe = (flow * 0.001) / self.d_pipe.get_area()
        return pump_val, geom_H, flow, speed_coll, speed_dpipe


def calculate(station, mode):
    """ Returns validation flag

    Runs calculations and checks if results exists and if are correct.
    """

    calculations = {'minimalisation': calc_minimalisation(),
                    'checking': calc_checking(),
                    'optimalisation': calc_optimalisation()}

    validation_flag = True
    n = calc_number_of_pumps()
    if n <= 0:
        validation_flag = False
    n = reserve_pumps_number()
    if n <= 0:
        validation_flag = False
    station.qp = station.get_calculative_flow()
    station.v_useful = check_get_useful_velo()
    station.h_useful = station.v_useful / station.well.cross_sectional_area()
    station.number_of_pumps = calc_number_of_pumps()
    station.number_of_res_pumps = reserve_pumps_number()
    station.ord_sw_on = station.ord_inlet.value - 0.1
    station.ord_sw_off = station.ord_bottom.value +\
        station.minimal_sewage_level.value
    station.ord_sw_alarm = station.ord_inlet.value
    station.height_start = station.height_to_pump(station.ord_sw_off)
    station.height_stop = station.height_to_pump(station.ord_sw_on)
    station.h_whole = station.ord_terrain.value - station.ord_bottom.value
    station.h_reserve = station.ord_sw_alarm - station.ord_sw_on
    station.v_whole = station.velocity(station.h_whole)
    station.v_dead = station.velocity(station.minimal_sewage_level.value)
    station.v_reserve = station.velocity(station.h_reserve)
    # TODO:
    # Calculations
    return validation_flag
