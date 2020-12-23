import pompa.models.variables as v
from pompa.exceptions import TooManyRootsError, NoRootsError
import numpy as np


class WorkPoint:
    """
    Class represent a work point - parameteres of pump set cooperating with
    set of pipes in station.
    """

    def __init__(self, geometric_height, ins_pipe_crossec_area,
                 out_pipe_crossec_area, pumpset_poly, pipeset_hydr_poly):
        self.geometric_height = geometric_height
        self.ins_pipe_crossec_area = ins_pipe_crossec_area
        self.out_pipe_crossec_area = out_pipe_crossec_area
        self.pumpset_poly = pumpset_poly
        self.pipeset_hydr_poly = pipeset_hydr_poly

    def _velocity(self, flow):
        """ Returns dict of velocity values in inside pipe and outside pipe.
        Expects instance od FlowVariable"""
        velocity = {}
        velocity['ins_pipe'] = round(
            flow.value_m3ps / self.ins_pipe_crossec_area, 2)
        velocity['out_pipe'] = round(
            flow.value_m3ps / self.out_pipe_crossec_area, 2)
        return velocity

    def _full_loss_poly(self):
        """To gotten array of polynomial coeefs describing pipe loss function,
        adds geometric height, and returns numpy-array-typed polynomial coeffs
        """
        res_poly = self.pipeset_hydr_poly.copy()
        res_poly[0] = self.pipeset_hydr_poly[0] + self.geometric_height.value
        return res_poly

    def calculate(self):
        """Returns parameters of workpoint.
        - Height of all loss [m]
        - Flow [FlovVariable]
        - Geometric height [m]
        - velocity in inside pipe [m/s]
        - velocity in outside pump [m/s]
        """
        pipeset_poly = self._full_loss_poly()

        """
        _36 = v.FlowVariable(36, 'lps')
        pumps_f = np.polynomial.polynomial.Polynomial(self.pumpset_poly)
        pipes_f = np.polynomial.polynomial.Polynomial(pipeset_poly)
        print('36: ', round(pumps_f(_36.value_m3ps), 2))
        print('36: ', round(pipes_f(_36.value_m3ps), 2))
        """

        all_roots = np.polynomial.polynomial.polyroots(
            self.pumpset_poly - pipeset_poly)
        # print('all roots: ', all_roots)
        roots = [np.real(i) for i in all_roots if np.isreal(i)]
        # print('roots real: ', roots)
        roots = [i for i in roots if i > 0]
        """
        print('roots > 0: ', roots)
        print('pipeset_poly ', pipeset_poly)
        print('pumpset_poly ', self.pumpset_poly)
        """
        if len(roots) > 1:
            raise TooManyRootsError(roots, pipeset_poly, self.pumpset_poly)
            return
        elif len(roots) == 0:
            raise NoRootsError(roots, pipeset_poly, self.pumpset_poly,
                               v.FlowVariable(11, 'lps'),
                               v.FlowVariable(22, 'lps'))
        flow = v.FlowVariable(roots[0], 'm3ps')
        height = np.polynomial.polynomial.Polynomial(
            self.pumpset_poly)(roots[0])
        velocity = self._velocity(flow)
        result = {'height': height, 'flow': flow,
                  'geom_h': self.geometric_height,
                  'ins_pipe_velo': velocity['ins_pipe'],
                  'out_pipe_velo': velocity['out_pipe']}
        print(result)
        return result
