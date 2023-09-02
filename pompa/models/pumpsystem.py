from pompa.models.pumpset import PumpSet
import math
from pompa.exceptions import ErrorContainer, WellTooShallowError,\
    NotEnoughPointsInPumpCharError, NotEnouthDataInPipeCharError,\
    IdealSmoothnessPipeError, TooManyRootsError, NoPumpsetError, \
    WellTooSmallError, InletInDeadVolumeError


PUMPSETS_LIMITER = 5


class PumpSystem:
    """Class used to keep Pumpsystem - all pumps in the station - calculations.

    Attributes
    ----------
    pumpsets : list
        List of pumpsets calculated iteratively until requirement of efficiency
        is fulfilled
    """

    def __init__(self, station, mode='checking'):
        """
        Parameters
        ----------
        station : Station
            The sewage pump station
        mode : str
            User-chosen mode of pumpsystem calculation (default = 'checking')
        """

        self.station = station
        self.enough_pumps = False
        self.pumpsets = []
        self.reserve_pumps = 0
        self.all_pumps = 0
        self.error_container = ErrorContainer()
        self.error_container.clear_errors()

        # Raising non-critical pre-calculations exceptions

        try:
            if not self.station.validate_dead_volume_under_inlet():
                raise InletInDeadVolumeError
        except InletInDeadVolumeError:
            pass

        self._calculate(mode)
        print('all pumps : ', self.all_pumps)

        # Raising non-critical post-calculations exceptions based on validators

        try:
            if not self.station.check_well_area_for_pumps(self.all_pumps):
                raise WellTooSmallError
        except WellTooSmallError:
            pass

    def _calculate(self, mode):
        """Made calculations based on chosen mode"""

        pick_method = {'checking': self._checking_mode}
        pick_method[mode]()

    def _checking_mode(self):
        """Calculate whether assumed bottom ordinate will let pump have
        appropriate cycle time in condition of least favorable inflow.
        """

        self.pumpsets = []
        enough_pumps = False
        self.ord_bottom = self.station.hydr_cond.ord_bottom
        self.ord_shutdown = self.station.pump_type.shutdown_ord(self.ord_bottom)
        pumps_counter = 0

        while not enough_pumps:
            pumps_counter += 1
            if len(self.pumpsets) == 0:
                last_pset = None
            else:
                last_pset = self.pumpsets[-1]
            try:
                self.pumpsets.append(PumpSet(self.station, self.ord_shutdown,
                                             pumps_counter, last_pset))
                if not self.data_validation():
                    raise NoPumpsetError
            except WellTooShallowError:
                break
            except NotEnouthDataInPipeCharError:
                break
            except NotEnoughPointsInPumpCharError:
                break
            except IdealSmoothnessPipeError:
                break
            except TooManyRootsError:
                break
            except NoPumpsetError:
                break
            print('pumpsets len: ', len(self.pumpsets))
            enough_pumps = self.pumpsets[-1].enough_pumps
            if pumps_counter == PUMPSETS_LIMITER:
                enough_pumps = True

        self.reserve_pumps = self._calc_reserve_pumps(pumps_counter)
        self._update_all_pumps_number()

    def _calc_reserve_pumps(self, working_pumps: int):
        mode = self.station.safety.value
        print(mode)
        if mode == 'economic':
            return 1
        elif mode == 'optimal':
            return math.ceil(working_pumps / 2)
        elif mode == 'safe':
            return working_pumps

    def _update_all_pumps_number(self):
        self.all_pumps = len(self.pumpsets) + self.reserve_pumps

    def calculate_volumes(self):
        area = self.station.well.cr_sec_area().get()
        total_h = self.station.hydr_cond.ord_terrain.get() - self.ord_bottom.get()
        useful_h = self.pumpsets[-1].ord_start.get() - self.ord_shutdown.get()
        reserve_h = self.station.hydr_cond.ord_inlet.get() - self.pumpsets[-1].ord_start.get()
        dead_h = self.station.pump_type.suction_level.get()
        total_v = round(total_h * area, 2)
        useful_v = round(useful_h * area, 2)
        reserve_v = round(reserve_h * area, 2)
        dead_v = round(dead_h * area, 2)

        return (total_v, useful_v, reserve_v, dead_v)

    def data_validation(self):
        validators = [self.station.pump_type.validate()]
        return all(validators)

