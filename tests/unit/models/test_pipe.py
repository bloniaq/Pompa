import pytest
import pompa.models.pipe as pipe
import pompa.models.variables as v
import numpy as np
from pompa.exceptions import FrictionFactorMethodOutOfRange

class TestPipe:

    @pytest.mark.parametrize('length, diameter, roughness, result', [
        (1.5, 0.1, 0.001, 0.104),
        (50, 0.11, 0.0015, 2.437)])
    def test_line_loss(self, length, diameter, roughness, result):
        pipe_obj = pipe.Pipe("test_tag")
        flow = pipe.v.FlowVariable(15, 'lps')
        pipe_obj.diameter.set(diameter)
        pipe_obj.roughness.set(roughness)
        pipe_obj.length.set(length)
        assert pipe_obj._line_loss(flow) == pytest.approx(result, rel=.01)

    def test_pipe_polynomial(self):
        pipe_obj = pipe.Pipe("test_tag")
        pipe_obj.length.set(100)
        pipe_obj.diameter.set(.150)
        pipe_obj.roughness.set(.0008)
        pipe_obj.resistances.set([0.27, 0.27, 0.6, 0.2, 2, 0.04])
        min_inflow = v.FlowVariable(5, 'lps')
        max_inflow = v.FlowVariable(40, 'lps')
        exp_array = np.array(
            [-6.86799e-03, -1.34499e+00, 3.91569385e+03])
        print(pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow))
        print(exp_array)
        np.testing.assert_almost_equal(
            pipe_obj.dynamic_loss_polynomial(
                min_inflow, max_inflow), exp_array, decimal=4)
    
    def test_init(self):
        pipe_obj = pipe.Pipe("test_tag")
        assert pipe_obj is not None


    @pytest.mark.parametrize('diameter, result', [
        (0.1, 0.0079),
        (0.110, 0.0095),
        (0.500, 0.1963),
        (0.050, 0.0020)])
    def test_area(self, diameter, result):
        pipe_obj = pipe.Pipe("test_tag")
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
    def test_velocity(self, diameter, flow, result):
        pipe_obj = pipe.Pipe("test_tag")
        pipe_obj.diameter.set(diameter)
        flow_var = pipe.v.FlowVariable(flow)
        assert pipe_obj._velocity(flow_var) == result


    @pytest.mark.parametrize('diameter, flow, result', [
        (0.125, 95, 266376),
        (0.200, 135.894, 238816),
        (0.250, 150, 210742),
        (0.300, 12.45, 14571)])
    def test_reynolds(self, diameter, flow, result):
        pipe_obj = pipe.Pipe("test_tag")
        pipe_obj.diameter.set(diameter)
        flow_var = pipe.v.FlowVariable(flow)
        assert pipe_obj._reynolds(flow_var) == result


    @pytest.mark.parametrize('reynolds, epsilon, result', [
        (6000, 0, 0.0359),
        (9000, 0, 0.0325),
        (90000, 0, 0.0183),
        (101000, 0.009, 0.0373),
        (189792, 0.01, 0.0379)])
    def test_lambda(self, reynolds, epsilon, result):
        pipe_obj = pipe.Pipe("test_tag")
        pipe_obj.diameter.set(0.100)
        pipe_obj.roughness.set(0.001)

        def fake_epsilon():
            return epsilon

        pipe_obj._epsilon = fake_epsilon

        assert pipe_obj._lambda(reynolds) == pytest.approx(result, abs=0.021)


    @pytest.mark.parametrize('velocity, loc_resists, result', [
        (1.91, [0.3, 0.5, 0.2, 0.1], 0.20),
        (1.58, [0.1, 0.1, 0.2], 0.05)])
    def test_local_loss(self, velocity, loc_resists, result):
        pipe_obj = pipe.Pipe("test_tag")
        pipe_obj.resistances.set(loc_resists)
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
    def test_dynamic_loss_poly(self, station_2, flow):
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
        v.FlowVariable(38.9, 'lps')])
    def test_dynamic_loss_poly_2(self, station_2, flow):
        pipe_obj = station_2.out_pipe

        min_inflow = v.FlowVariable(10, 'lps')
        max_inflow = v.FlowVariable(22.2, 'lps')

        exp_coeffs = np.array([0.055, -5.441, 1193.416])
        exp_height = np.polynomial.polynomial.Polynomial(exp_coeffs)(
            flow.value_m3ps)

        coeffs = pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow, 2)
        height = np.polynomial.polynomial.Polynomial(coeffs)(
            flow.value_m3ps)

        assert exp_height == pytest.approx(height, rel=0.05)

    @pytest.mark.parametrize('flow', [
        v.FlowVariable(8, 'lps'),
        v.FlowVariable(10, 'lps'),
        v.FlowVariable(12, 'lps'),
        v.FlowVariable(14, 'lps'),
        v.FlowVariable(16, 'lps'),
        v.FlowVariable(18, 'lps'),
        v.FlowVariable(20, 'lps'),
        v.FlowVariable(22.2, 'lps'),
        v.FlowVariable(28, 'lps')])
    def test_dynamic_loss_poly_parallels(self, station_3, flow):
        pipe_obj = station_3.out_pipe

        min_inflow = v.FlowVariable(5, 'lps')
        max_inflow = v.FlowVariable(30, 'lps')

        # stare wartości
        # exp_coeffs = np.array([0.269, -29.808, 7153.488])
        #
        # https://www.omnicalculator.com/physics/friction-loss
        # https://arachnoid.com/polysolve/
        # exp_coeffs = np.array([-2.9114989276888714e-002, 2.2274416445179924e+001, 4.4774217006891686e+003])
        #
        # stara pompa
        # https://arachnoid.com/polysolve/
        exp_coeffs = np.array([-4.1344071227009582e-001, 5.1392397030049608e+001, 4.6214326748354915e+003])
        # 3 kalkulatory
        # https://www.pipeflowcalculations.com/reynolds/calculator.xhtml
        # https://www.omnicalculator.com/physics/friction-factor
        # https://www.engineeringtoolbox.com/darcy-weisbach-equation-d_646.html
        # https://arachnoid.com/polysolve/
        # exp_coeffs = np.array([-2.8833541534732277e-002, 2.3765701501814021e+001, 4.8023228278361275e+003])



        exp_height = np.polynomial.polynomial.Polynomial(exp_coeffs)(
            flow.value_m3ps)

        coeffs = pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow, 2)
        height = np.polynomial.polynomial.Polynomial(coeffs)(
            flow.value_m3ps)

        assert exp_height == pytest.approx(height, rel=0.18)


class TestFrictionFactor:

    def test_comaparision_2(self, friction_factor_turbulent_smooth_cond):
        factor = friction_factor_turbulent_smooth_cond
        expected_result = {
            'colebrook-white': 0.0269,
            'walden': (0.0264, 'OUT OF RANGE'),
            'hagen-poiseuille': (0.0032, 'OUT OF RANGE'),
            'blasius': 0.0266,
            'haaland': 0.0267,
            'bellos-nalbantis-tsakiris': 0.0262,
            'cheng': 0.0256,
            'wood': 0.0267,
            'swamee-jain': 0.0270,
            'churchill': 0.0270,
            'mitosek': 0.0266
        }
        assert factor._FrictionFactor__comparision() == expected_result

    def test_comparision_laminar(self, friction_factor_laminar):
        factor = friction_factor_laminar
        expected_result = {
            'colebrook-white': (0.0656, 'OUT OF RANGE'),
            'walden': (0.0686, 'OUT OF RANGE'),
            'hagen-poiseuille': 0.0640,
            'blasius': (0.0563, 'OUT OF RANGE'),
            'haaland': (0.0686, 'OUT OF RANGE'),
            'bellos-nalbantis-tsakiris': 0.0640,
            'cheng': 0.0640,
            'wood': (0.0661, 'OUT OF RANGE'),
            'swamee-jain': (0.0698, 'OUT OF RANGE'),
            'churchill': 0.0640,
            'mitosek': 0.064
        }
        assert factor._FrictionFactor__comparision() == expected_result

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
        assert isinstance(factor._methods, dict)

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
