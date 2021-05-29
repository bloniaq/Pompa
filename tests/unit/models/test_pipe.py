import pytest
import pompa.models.pipe as pipe
import pompa.models.variables as v
import numpy as np
from pompa.exceptions import FrictionFactorMethodOutOfRange


def test_init():
    pipe_obj = pipe.Pipe()
    assert pipe_obj is not None


@pytest.mark.parametrize('diameter, result', [
    (0.1, 0.0079),
    (0.110, 0.0095),
    (0.500, 0.1963),
    (0.050, 0.0020)])
def test_area(diameter, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(diameter)
    assert pipe_obj.area() == result


@pytest.mark.parametrize('diameter, flow, result', [
    (0.09978, 1, 0.0354),
    (0.125, 0.99, 0.0220),
    (0.31000001, 1.36889, 0.005),
    (0.075, 2.54877, 0.1614),
    (0.090, 1.45, 0.0625),
    (0.125, 145, 3.2748),
    (0.125, 94.78, 2.1407)])
def test_velocity(diameter, flow, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(diameter)
    flow_var = pipe.v.FlowVariable(flow)
    assert pipe_obj._velocity(flow_var) == result


@pytest.mark.parametrize('diameter, flow, result', [
    (0.125, 95, 266376),
    (0.200, 135.894, 238816),
    (0.250, 150, 210742),
    (0.300, 12.45, 14571)])
def test_reynolds(diameter, flow, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(diameter)
    flow_var = pipe.v.FlowVariable(flow)
    assert pipe_obj._reynolds(flow_var) == result


@pytest.mark.parametrize('reynolds, epsilon, result', [
    (6000, 0, 0.0359),
    (9000, 0, 0.0325),
    (90000, 0, 0.0183),
    (101000, 0.009, 0.0373),
    (189792, 0.01, 0.0379)])
def test_lambda(reynolds, epsilon, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(0.100)
    pipe_obj.roughness.set(0.001)

    def fake_epsilon():
        return epsilon

    pipe_obj._epsilon = fake_epsilon

    assert pipe_obj._lambda(reynolds) == pytest.approx(result, abs=0.021)


@pytest.mark.parametrize('velocity, loc_resists, result', [
    (1.91, [0.3, 0.5, 0.2, 0.1], 0.20),
    (1.58, [0.1, 0.1, 0.2], 0.05)])
def test_local_loss(velocity, loc_resists, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.resistance.set(loc_resists)
    _ = 0

    def fake_velocity(_):
        return velocity

    pipe_obj._velocity = fake_velocity
    assert pipe_obj._local_loss(_) == result


@pytest.mark.parametrize('flow', [
    v.FlowVariable(17, 'lps'),
    v.FlowVariable(21, 'lps'),
    v.FlowVariable(26, 'lps'),
    v.FlowVariable(30, 'lps'),
    v.FlowVariable(36, 'lps'),
    v.FlowVariable(42, 'lps'),
    v.FlowVariable(51, 'lps'),
    v.FlowVariable(8, 'lps'),
    v.FlowVariable(12, 'lps'),
    v.FlowVariable(45, 'lps')])
def test_dynamic_loss_poly(station_2, flow):
    pipe_obj = station_2.out_pipe

    min_inflow = v.FlowVariable(11, 'lps')
    max_inflow = v.FlowVariable(22, 'lps')

    exp_coeffs = np.array([0.055, -10.083, 4773.663, 0])
    exp_height = np.polynomial.polynomial.Polynomial(exp_coeffs)(
        flow.value_m3ps)

    coeffs = pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow)
    height = np.polynomial.polynomial.Polynomial(coeffs)(
        flow.value_m3ps)

    assert exp_height == pytest.approx(height, rel=0.008, abs=0.02)


@pytest.mark.parametrize('flow', [
    v.FlowVariable(16.7, 'lps'),
    v.FlowVariable(19.4, 'lps'),
    v.FlowVariable(22.2, 'lps'),
    v.FlowVariable(25, 'lps'),
    v.FlowVariable(27.8, 'lps'),
    v.FlowVariable(30.6, 'lps'),
    v.FlowVariable(33.3, 'lps'),
    v.FlowVariable(36.1, 'lps'),
    v.FlowVariable(38.9, 'lps'),
    v.FlowVariable(8, 'lps')])
def test_dynamic_loss_poly_2(station_2, flow):
    pipe_obj = station_2.out_pipe

    min_inflow = v.FlowVariable(10, 'lps')
    max_inflow = v.FlowVariable(22.2, 'lps')

    exp_coeffs = np.array([0.055, -5.441, 1193.416, 0])
    exp_height = np.polynomial.polynomial.Polynomial(exp_coeffs)(
        flow.value_m3ps)

    coeffs = pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow, 2)
    height = np.polynomial.polynomial.Polynomial(coeffs)(
        flow.value_m3ps)

    assert exp_height == pytest.approx(height, rel=0.008, abs=0.02)


@pytest.mark.parametrize('flow', [
    v.FlowVariable(10, 'lps'),
    v.FlowVariable(12, 'lps'),
    v.FlowVariable(14, 'lps'),
    v.FlowVariable(16, 'lps'),
    v.FlowVariable(18, 'lps'),
    v.FlowVariable(20, 'lps'),
    v.FlowVariable(22.2, 'lps'),
    v.FlowVariable(8, 'lps'),
    v.FlowVariable(28, 'lps')])
def test_dynamic_loss_poly_parallels(station_3, flow):
    pipe_obj = station_3.out_pipe

    min_inflow = v.FlowVariable(10, 'lps')
    max_inflow = v.FlowVariable(22.2, 'lps')

    exp_coeffs = np.array([0.269, -29.808, 7153.488, 0])
    exp_height = np.polynomial.polynomial.Polynomial(exp_coeffs)(
        flow.value_m3ps)

    coeffs = pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow, 2)
    height = np.polynomial.polynomial.Polynomial(coeffs)(
        flow.value_m3ps)

    assert exp_height == pytest.approx(height, rel=0.04, abs=0.04)


class TestFrictionFactor:

    @pytest.fixture
    def friction_factor_base(self):
        diameter = v.FloatVariable(.200)
        roughness = v.FloatVariable(.1)
        reynolds = 150000
        factor = pipe.FrictionFactor(diameter, roughness, reynolds)
        return factor

    def test_init_existing(self, friction_factor_base):
        factor = friction_factor_base
        assert factor is not None

    def test_existing_method_dict(self, friction_factor_base):
        factor = friction_factor_base
        assert isinstance(factor.methods, dict)

    def test_walden_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor._walden() == 0.3284

    def test_call_walden_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor('walden') == 0.3284

    def test_walden_out_of_range(self, friction_factor_laminar):
        factor = friction_factor_laminar
        with pytest.raises(FrictionFactorMethodOutOfRange):
            factor('walden')

    def test__out_of_range(self, friction_factor_laminar):
        factor = friction_factor_laminar
        with pytest.raises(FrictionFactorMethodOutOfRange):
            factor('colebrook-white')

    def test_comparision_base(self, friction_factor_base):
        factor = friction_factor_base
        expected_result = {
            'colebrook-white': 0.3292,
            'walden': 0.3284,
            'hagen-poiseuille': (0.0004, 'OUT OF RANGE'),
            'blasius': (0.0161, 'OUT OF RANGE'),
            'haaland': 0.3317,
            'bellos-nalbantis-tsakiris': 0.3503,
            'cheng': 0.3309,
            'wood': (0.3454, 'OUT OF RANGE'),
            'swamee-jain': (0.3312, 'OUT OF RANGE'),
            'churchill': 0.3308,
            'mitosek': 0.33
        }
        assert factor._FrictionFactor__comparision() == expected_result

    def test_hagen_poiseuille(self, friction_factor_base):
        factor = friction_factor_base
        with pytest.raises(FrictionFactorMethodOutOfRange):
            factor('hagen-poiseuille')

    def test_hagen_poiseuille_laminar(self, friction_factor_laminar):
        factor = friction_factor_laminar
        assert factor('hagen-poiseuille') == 0.064

    def test_blasius_turb_smooth_cond(self,
                                      friction_factor_turbulent_smooth_cond):
        factor = friction_factor_turbulent_smooth_cond
        assert factor('blasius') == 0.0266

    def test_haaland_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor('haaland') == 0.3317

    def test_bnt_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor('bellos-nalbantis-tsakiris') == 0.3503

    def test_cheng_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor('cheng') == 0.3309

    def test_wood_base(self, friction_factor_base):
        factor = friction_factor_base
        with pytest.raises(FrictionFactorMethodOutOfRange):
            factor('wood')

    def test_swamee_jain_base(self, friction_factor_base):
        factor = friction_factor_base
        with pytest.raises(FrictionFactorMethodOutOfRange):
            factor('swamee-jain')

    def test_churchill_base(self, friction_factor_base):
        factor = friction_factor_base
        assert factor('churchill') == 0.3308
