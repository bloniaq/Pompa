import pompa.models.variables as v
from pompa.exceptions import TooManyRootsError, NoRootsError
import numpy as np


class WorkPoint:
    """
    Class represent a work point - parameteres of pump set cooperating with
    set of pipes in station.

    Public parameters:
        self.height
        self.flow
        self.geometric_height
        self.ins_pipe_v
        self.out_pipe_v
    """

    def __init__(self, geometric_height, ins_pipe_crossec_area,
                 out_pipe_crossec_area, pumpset_poly, pipeset_hydr_poly):
        # parameters
        self._ins_pipe_crossec_area = ins_pipe_crossec_area
        self._out_pipe_crossec_area = out_pipe_crossec_area
        self._pumpset_poly = pumpset_poly
        # print('pumpset poly: ', pumpset_poly)
        self._pipeset_hydr_poly = pipeset_hydr_poly

        # interface
        self.height = None
        self.flow = None
        self.geom_h = geometric_height
        self.ins_pipe_v = None
        self.out_pipe_v = None

        # calculations
        (self.height, self.flow,
            self.ins_pipe_v, self.out_pipe_v) = self._calculate()

    def __repr__(self):
        string = 'WPoint (Q: ' + str(
            self.flow.value_lps) + ' lps; H: ' + str(self.height) + ' m)'
        return string

    def _velocity(self, flow):
        """ Returns dict of velocity values in inside pipe and outside pipe.
        Expects instance od FlowVariable"""
        velocity = {}
        velocity['ins_pipe'] = round(
            flow.value_m3ps / self._ins_pipe_crossec_area, 2)
        velocity['out_pipe'] = round(
            flow.value_m3ps / self._out_pipe_crossec_area, 2)
        return velocity

    def _full_loss_poly(self):
        """To gotten array of polynomial coeefs describing pipe loss function,
        adds geometric height, and returns numpy-array-typed polynomial coeffs
        """
        res_poly = self._pipeset_hydr_poly.copy()
        # print('dynamic poly: ', res_poly)
        res_poly[0] = self._pipeset_hydr_poly[0] + self.geom_h.value
        # print('full loss poly: ', res_poly)
        return res_poly

    def _calculate(self):
        """Returns parameters of workpoint.
        - Height of all loss [m]
        - Flow [FlovVariable]
        - Geometric height [m]
        - velocity in inside pipe [m/s]
        - velocity in outside pump [m/s]
        """
        pipeset_poly = self._full_loss_poly()

        all_roots = np.polynomial.polynomial.polyroots(
            self._pumpset_poly - pipeset_poly)
        roots = [np.real(i) for i in all_roots if np.isreal(i)]
        roots = [i for i in roots if i > 0]

        if len(roots) > 1:
            raise TooManyRootsError(roots, pipeset_poly, self._pumpset_poly)
            return
        elif len(roots) == 0:
            raise NoRootsError(roots, pipeset_poly, self._pumpset_poly,
                               v.FlowVariable(11, 'lps'),
                               v.FlowVariable(22, 'lps'))
        flow = v.FlowVariable(roots[0], 'm3ps')
        height = np.polynomial.polynomial.Polynomial(
            self._pumpset_poly)(roots[0])
        velocity = self._velocity(flow)
        # print(height, flow, velocity['ins_pipe'], velocity['out_pipe'])
        return height, flow, velocity['ins_pipe'], velocity['out_pipe']
