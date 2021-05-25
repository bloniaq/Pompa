import pytest
import numpy as np
import pompa.models.pipe as pipe
import pompa.models.variables as v


class TestPipe:

    @pytest.mark.parametrize('length, diameter, roughness, result', [
        (1.5, 0.1, 0.001, 0.104),
        (50, 0.11, 0.0015, 2.437)])
    def test_line_loss(self, length, diameter, roughness, result):
        pipe_obj = pipe.Pipe()
        flow = pipe.v.FlowVariable(15, 'lps')
        pipe_obj.diameter.set(diameter)
        pipe_obj.roughness.set(roughness)
        pipe_obj.length.set(length)
        assert pipe_obj._line_loss(flow) == pytest.approx(result, rel=.01)

    def test_pipe_polynomial(self):
        pipe_obj = pipe.Pipe()
        pipe_obj.length.set(100)
        pipe_obj.diameter.set(.150)
        pipe_obj.roughness.set(.0008)
        pipe_obj.resistance.set([0.27, 0.27, 0.6, 0.2, 2, 0.04])
        pipe_obj.parallels.set(1)
        min_inflow = v.FlowVariable(5, 'lps')
        max_inflow = v.FlowVariable(40, 'lps')
        exp_array = np.array(
            [-6.86799e-03, -1.34499e+00, 3.91569385e+03, 0.00000e+00])
        print(pipe_obj.dynamic_loss_polynomial(min_inflow, max_inflow))
        print(exp_array)
        np.testing.assert_almost_equal(
            pipe_obj.dynamic_loss_polynomial(
                min_inflow, max_inflow), exp_array, decimal=4)


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
