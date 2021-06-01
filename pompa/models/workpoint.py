import pompa.models.variables as v
from pompa.exceptions import TooManyRootsError, NoRootsError
import numpy as np


class WorkPoint:
    """
    Class used to represent a pump Workpoint.

    Workpoint is an equilibrium point between line losses and pump lifting
    height calculated for a specific ordinate of sewage. Ordinates of this
    point are calculated based on root of difference of two polynomials

    Attributes
    ----------
    height : FloatVariable
        The value of pump lifting height [m]
    flow : FlowVariable
        The value of pump flow [m3ph, m3ps, lps]
    geometric_height : FloatVariable
        Geometric height to pump - difference between ordinates of end of
        pressurized pipe and sewage level in pump station
    ins_pipe_v : float
        Sewage velocity in pipe(s) inside station
    out_pipe_v : float
        Sewage velocity in pipe(s) outside station
    """

    def __init__(self, geometric_height, ins_pipe_crossec_area,
                 out_pipe_crossec_area, pumpset_poly, pipeset_hydr_poly,
                 ins_pipes_no=1, out_pipes_no=1):
        """
        Parameters
        ----------
        geometric_height : FloatVariable
        ins_pipe_crossec_area : float
            Cross-sectional area of pipe(s) inside pump station
        out_pipe_crossec_area : float
            Cross-sectional area of pipe(s) outside pump station
        pumpset_poly : numpy.ndarray
            3rd grade polynomial of pump characteristic
        pipeset_hydr_poly : numpy.ndarray
            3rd grade polynomial of dynamic losses in pipeset
        ins_pipes_no=1 : int, optional
            The number of pipes inside station (equals number of pumps)
        out_pipes_no=1 : int, optional
            The number of pipes outside station
        """

        # private attributes
        self._ins_pipe_crossec_area = ins_pipe_crossec_area
        self._out_pipe_crossec_area = out_pipe_crossec_area
        self._pumpset_poly = pumpset_poly
        self._pipeset_hydr_poly = pipeset_hydr_poly
        self._ins_pipes_no = ins_pipes_no
        self._out_pipes_no = out_pipes_no

        # interface declarations
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
        """Return dict of velocity values of inside pipe and outside pipe.

        Velocity is calculated as division of flow [m3ps] by cross-sectional
        area of pipe [m2]. Result is dictionary of velocities in inside and
        outside pipes

        Parameters
        ----------
        flow : FlowVariable
            Value of pumping flow in workpoint

        Returns
        -------
        dict
            a dictionary of velocities in inside ('ins_pipe') and outside
            ('out_pipe') pipes
        """
        velocity = {}
        velocity['ins_pipe'] = round(flow.value_m3ps / (
            self._ins_pipe_crossec_area * self._ins_pipes_no), 2)
        velocity['out_pipe'] = round(flow.value_m3ps / (
            self._out_pipe_crossec_area * self._out_pipes_no), 2)
        return velocity

    def _full_loss_poly(self):
        """Return pipeset polynomial including geometric height

        Gotten array of polynomial coefs describing pipeset loss function is
        increment by geometric height
        """
        res_poly = self._pipeset_hydr_poly.copy()
        res_poly[0] = self._pipeset_hydr_poly[0] + self.geom_h.value
        return res_poly

    def _calculate(self):
        """Return parameters of workpoint.

        Flow and Height parameters are ordinates of cross point of pipe- and
        pump- polynomials. First are find roots of subtraction one poly
        from another. It is resulted flow Then, there is calculation of value
        of pump poly in founded root, which is height of workpoint.

        Raises
        ------
        TooManyRootsError
            If subtraction resulted polynomial has more then one zero
        NoRootsError
            If subtraction resulted polynomial has no zeros

        Returns
        -------
        height : float
            The value of pump lifting height [m]
        flow : FlowVariable
            The value of pump flow [m3ph, m3ps, lps]
        velocity['ins_pipe'] : float
            The velocity in inside pipe [m/s]
        velocity['out_pipe']
            The velocity in outside pump [m/s]
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
        return height, flow, velocity['ins_pipe'], velocity['out_pipe']
