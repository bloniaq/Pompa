import pompa.models.variables as v
from pompa.exceptions import TooManyRootsError
import numpy as np


class WorkPoint:
    """
    Class represent a work point - parameteres of pump set cooperating with
    set of pipes in station.
    """

    def __init__(self, pumpset_amount, geometric_height, ins_pipe_crossec_area,
                 out_pipe_crossec_area, pumpset_poly, pipeset_hydr_poly):
        self.pumpset_amount = pumpset_amount
        self.geometric_height = geometric_height
        self.ins_pipe_crossec_area = ins_pipe_crossec_area
        self.out_pipe_crossec_area = out_pipe_crossec_area
        self.pumpset_poly = pumpset_poly
        self.pipeset_hydr_poly = pipeset_hydr_poly

    def _speed(self, flow):
        """ Returns dict of speed values in inside pipe and outside pipe.
        Expects instance od FlowVariable"""
        speed = {}
        speed['ins_pipe'] = round(
            flow.value_m3ps / self.ins_pipe_crossec_area, 2)
        speed['out_pipe'] = round(
            flow.value_m3ps / self.out_pipe_crossec_area, 2)
        return speed

    def _full_loss_poly(self):
        """To gotten array of polynomial coeefs describing pipe loss function,
        adds geometric height, and returns numpy-array-typed polynomial coeffs
        """
        result_poly = self.pipeset_hydr_poly
        result_poly[0] = self.pipeset_hydr_poly[0] + self.geometric_height
        return result_poly

    def calculate(self):
        """Returns parameters of workpoint.
        - Height of all loss [m]
        - Flow [FlovVariable]
        - Geometric height [m]
        - Speed in inside pipe [m/s]
        - Speed in outside pump [m/s]
        """
        pipeset_poly = self._full_loss_poly()
        all_roots = np.polynomial.polynomial.polyroots(
            self.pumpset_poly - pipeset_poly)
        roots = [np.real(i) for i in all_roots if np.isreal(i)]
        if len(roots) > 1:
            raise TooManyRootsError
            return
        flow = v.FlowVariable(roots[0], 'm3ps')
        height = np.polynomial.polynomial.Polynomial(
            self.pumpset_poly)(roots[0])
        speed = self._speed(flow)
        return (
            height, flow, self.geometric_height, speed['ins_pipe'],
            speed['out_pipe'])
