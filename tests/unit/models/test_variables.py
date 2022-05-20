import pompa.models.variables as variables
from pompa.exceptions import InputTypeError
import pytest
import numpy as np
from unittest.mock import Mock


class TestVariable:

    fixture_list = [
        'variable_no_value',
        'variable_integer',
        'variable_float',
        'variable_boolean',
        'variable_string']

    @pytest.fixture
    def variable_no_value(self, request):
        """Returns a Variable instance with default value"""
        return variables.Variable()

    @pytest.fixture
    def variable_integer(self, request):
        return variables.Variable(5)

    @pytest.fixture
    def variable_float(self, request):
        return variables.Variable(13.0)

    @pytest.fixture
    def variable_boolean(self, request):
        return variables.Variable(True)

    @pytest.fixture
    def variable_string(self, request):
        return variables.Variable('test string')

    def test_var_init_default(self):
        var = variables.Variable()
        assert var.value is None

    @pytest.mark.parametrize('value', [
        5, 13.0, True, 'test string'])
    def test_var_init_vals(self, value):
        var = variables.Variable(value)
        assert var.value == value

    @pytest.mark.parametrize('fixture', fixture_list)
    def test_add_callback(self, fixture, request):
        func_expecting_callback = Mock()
        var = request.getfixturevalue(fixture)
        var.add_callback(func_expecting_callback)
        print(var.callbacks.keys())
        assert list(var.callbacks.keys()) == [func_expecting_callback]

    @pytest.mark.parametrize('fixture', fixture_list)
    @pytest.mark.parametrize('new_value', [15.0, False, 'test string', 4])
    def test_var_set_val_change(self, fixture, new_value, request):
        var = request.getfixturevalue(fixture)
        var.set(new_value)
        assert var.value == new_value

    @pytest.mark.parametrize('fixture', fixture_list)
    @pytest.mark.parametrize('new_value', [15.0, False, 'test string', 4])
    def test_var_set_callbacks(self, fixture, new_value, request):
        var = request.getfixturevalue(fixture)
        func_expecting_callback = Mock()
        var.add_callback(func_expecting_callback)
        var.set(new_value)
        func_expecting_callback.assert_called()

    @pytest.mark.parametrize('fixture', fixture_list)
    @pytest.mark.parametrize('new_value', [15.0, False, 'test string', 4])
    def test_var_get(self, fixture, new_value, request):
        var = request.getfixturevalue(fixture)
        var.set(new_value)
        assert var.get() == new_value

    def test_get_var(self):
        var = variables.FloatVariable(45, name='test_name')
        result = variables.Variable.get_var('test_name')
        assert result is var


class TestFloatVar():

    @pytest.fixture
    def float_var_no_val(self, request):
        '''Returns a basic FloatVariable with no value'''
        return variables.FloatVariable()

    @pytest.fixture
    def float_var_value_20(self, request):
        '''Returns a basic FloatVariable with value of 20'''
        return variables.FloatVariable(20)

    @pytest.mark.parametrize(
        'fixture', ['float_var_no_val', 'float_var_value_20'])
    def test_init(self, fixture, request):
        assert request.getfixturevalue(fixture) is not None

    def test_init_convert(self, float_var_value_20):
        assert isinstance(float_var_value_20.value, float)

    def test_string_input_value(self):
        with pytest.raises(InputTypeError):
            variables.FloatVariable("test string")

    @pytest.mark.parametrize(
        'fixture', ['float_var_no_val', 'float_var_value_20'])
    def test_float_instance(self, fixture, request):
        assert isinstance(request.getfixturevalue(fixture).value, float)

    @pytest.mark.parametrize(
        'fixture', ['float_var_no_val', 'float_var_value_20'])
    def test_set_float_value(self, fixture, request):
        float_var = request.getfixturevalue(fixture)
        float_val = 34.56
        float_var.set(float_val)
        assert float_var.value == float_val

    @pytest.mark.parametrize(
        'fixture', ['float_var_no_val', 'float_var_value_20'])
    def test_set_int_value(self, fixture, request):
        float_var = request.getfixturevalue(fixture)
        int_val = 7
        float_var.set(int_val)
        assert float_var.value == 7.00

    @pytest.mark.parametrize(
        'fixture', ['float_var_no_val', 'float_var_value_20'])
    def test_set_string_value(self, fixture, request):
        float_var = request.getfixturevalue(fixture)
        string_val = 'test string'
        with pytest.raises(InputTypeError):
            float_var.set(string_val)

    def test_digits(self):
        float_var = variables.FloatVariable(0.458593211, 3)
        assert float_var.value == 0.459

    def test_digits_with_default_value(self):
        float_var = variables.FloatVariable(digits=5)
        float_var.set(0.423672945)
        assert float_var.value == 0.42367

    def test_add(self):
        float1 = variables.FloatVariable(24.8)
        float2 = variables.FloatVariable(3.17)
        assert float1 + float2 == variables.FloatVariable(27.97)
        assert float1 + float2 is float1

    def test_mul(self):
        float1 = variables.FloatVariable(13)
        float2 = variables.FloatVariable(2)
        assert float1 * float2 == variables.FloatVariable(26)
        # assert float1 * float2 is float1


class Test_IntVar:

    @pytest.fixture
    def int_var_no_val(self, request):
        '''Returns a basic FloatVariable with no value'''
        return variables.IntVariable()

    @pytest.fixture
    def int_var_value_20(self, request):
        '''Returns a basic FloatVariable with value of 20'''
        return variables.IntVariable(20)

    @pytest.mark.parametrize(
        'fixture', ['int_var_no_val', 'int_var_value_20'])
    def test_init(self, fixture, request):
        assert request.getfixturevalue(fixture) is not None

    def test_init_convert(self):
        var = variables.IntVariable(32.02)
        assert isinstance(var.value, int)

    def test_string_input_value(self):
        with pytest.raises(ValueError):
            variables.IntVariable("test string")

    @pytest.mark.parametrize(
        'fixture', ['int_var_no_val', 'int_var_value_20'])
    def test_int_instance(self, fixture, request):
        assert isinstance(request.getfixturevalue(fixture).value, int)

    @pytest.mark.parametrize(
        'fixture', ['int_var_no_val', 'int_var_value_20'])
    @pytest.mark.parametrize(
        'float_val, result', [(5.66, 6), (4.50, 4), (5.5, 6), (3.24, 3)])
    def test_set_float_value(self, fixture, float_val, result, request):
        int_var = request.getfixturevalue(fixture)
        int_var.set(float_val)
        assert int_var.value == result

    @pytest.mark.parametrize(
        'fixture', ['int_var_no_val', 'int_var_value_20'])
    def test_set_string_value(self, fixture, request):
        int_var = request.getfixturevalue(fixture)
        string_val = 'test string'
        with pytest.raises(InputTypeError):
            int_var.set(string_val)

    def test_int_inheritance(self):
        var_1 = variables.IntVariable(4)
        var_2 = variables.IntVariable(8)
        assert var_1 < var_2
        assert var_2 > var_1
        assert var_2 + var_1 == 12
        assert var_2 - var_1 == 4


class Test_FlowVar:

    fixture_list = [
        'flow_default',
        'flow_20_defaultunit',
        'flow_35_m3ph',
        'flow_13_lps']

    fixtures_expected_attributes = [
        (0, 'm3ph', 0.00, 0.00),
        (20, 'm3ph', 20.00, 5.56),
        (35, 'm3ph', 35.00, 9.72),
        (13, 'lps', 46.80, 13.00)]
    #  init_value, init_unit, m3ph_value, lps_value

    @pytest.fixture
    def flow_default(self, request):
        '''Returns FlowVar instance initialised without start value
        '''
        return variables.FlowVariable()

    @pytest.fixture
    def flow_20_defaultunit(self, request):
        '''Returns FlowVar instance initialised as 20 of default unit'''
        return variables.FlowVariable(20)

    @pytest.fixture
    def flow_35_m3ph(self, request):
        '''Returns FlowVar instance initialised as 35 m3ph'''
        return variables.FlowVariable(35, 'm3ph')

    @pytest.fixture
    def flow_13_lps(self, request):
        '''Returns FlowVar instance initialised as 13 lps'''
        return variables.FlowVariable(13, 'lps')

    @pytest.mark.parametrize('fixture', fixture_list)
    def test_init(self, fixture, request):
        assert request.getfixturevalue(fixture) is not None

    @pytest.mark.parametrize('fixture, expected_args', zip(
        fixture_list, fixtures_expected_attributes))
    def test_init_units(self, fixture, expected_args, request):
        flow_var = request.getfixturevalue(fixture)
        assert flow_var.init_unit == expected_args[1]

    @pytest.mark.parametrize('fixture, expected_args', zip(
        fixture_list, fixtures_expected_attributes))
    def test_init_values(self, fixture, expected_args, request):
        flow_var = request.getfixturevalue(fixture)
        assert flow_var.value_m3ph == expected_args[2]
        assert flow_var.value_lps == expected_args[3]

    @pytest.mark.parametrize('fixture', fixture_list)
    @pytest.mark.parametrize('value, unit, expected_m3ph, expected_lps', [
        (41, 'lps', 147.60, 41.00),
        (3.5, 'm3ph', 3.50, 0.97),
        (14.86, 'lps', 53.50, 14.86),
        (17.975, 'm3ph', 17.98, 4.99),
        (17.984, 'm3ph', 17.98, 5.00)])
    def test_set(
        self, fixture, value, unit, expected_m3ph, expected_lps, request
    ):
        flow_var = request.getfixturevalue(fixture)
        flow_var.set(value, unit)
        assert flow_var.value_m3ph == expected_m3ph
        assert flow_var.value_lps == expected_lps

    @pytest.mark.parametrize('fixture', fixture_list)
    def test_set_string(self, fixture, request):
        flow_var = request.getfixturevalue(fixture)
        with pytest.raises(InputTypeError):
            flow_var.set("test string")

    def test_m3ps(self):
        flow_var = variables.FlowVariable(34, 'lps')
        assert flow_var._m3ps(flow_var.value_lps) == 0.034
        assert flow_var.value_m3ps == 0.034


class Test_SwitchVar:

    fixture_list = [
        'sw_var_no_args',
        'sw_var_value_nodict',
        'sw_var_value_dict']

    @pytest.fixture
    def sw_var_no_args(self, request):
        '''Returns SwitchVariable initialized with no arguments'''
        return variables.SwitchVariable()

    @pytest.fixture
    def sw_var_value_nodict(self, request):
        '''Retruns SwitchVariable initialized with value but no dict argument
        '''
        return variables.SwitchVariable('test string')

    @pytest.fixture
    def sw_var_value_dict(self, request):
        '''Returns SwitchVariable initialized with value and dict argument'''
        return variables.SwitchVariable('True', {'1': True, '0': False})

    @pytest.mark.parametrize('fixture', fixture_list)
    def test_init_noargs(self, fixture, request):
        switch_var = request.getfixturevalue(fixture)
        assert switch_var is not None
        assert switch_var.dictionary is not None


class Test_ResistanceVar:

    def test_init(self):
        assert variables.ResistanceVariable() is not None
        assert variables.ResistanceVariable().value == []

    def test_set_from_a_list(self):
        res_var = variables.ResistanceVariable()
        res_var.set([0.5, 0.43])
        assert res_var.value == [0.5, 0.43]

    def test_sum(self):
        res_var = variables.ResistanceVariable([0.1, 0.2, 0.333])
        assert res_var.sum() == 0.633


class Test_PumpCharVar:

    def test_init(self):
        assert variables.PumpCharVariable() is not None

    def test_add_point(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(35.56, 12.34)
        expected_flow = variables.FlowVariable(35.56)
        assert characteristic.value == [(expected_flow, 12.34)]

    def test_add_point_in_lps_unit(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(35.56, 12.34, 'lps')
        expected_flow = variables.FlowVariable(35.56, 'lps')
        assert characteristic.value == [(expected_flow, 12.34)]

    def test_remove_point(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(35.56, 12.34)
        characteristic.add_point(12.01, 11.95, 'lps')
        characteristic.add_point(33.4, 13.03)
        expected_flow_1 = variables.FlowVariable(35.56)
        expected_flow_2 = variables.FlowVariable(12.01, 'lps')
        expected_flow_3 = variables.FlowVariable(33.4)
        point_to_remove = (expected_flow_2, 11.95)
        characteristic.remove_point(point_to_remove)
        assert characteristic.value == [
            (expected_flow_3, 13.03),
            (expected_flow_1, 12.34)]

    def test_sorting_characteristic(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(35.56, 12.34)
        characteristic.add_point(36.05, 11.95)
        characteristic.add_point(33.4, 13.03)
        exp_point_1 = (variables.FlowVariable(35.56), 12.34)
        exp_point_2 = (variables.FlowVariable(36.05), 11.95)
        exp_point_3 = (variables.FlowVariable(33.4), 13.03)
        assert characteristic.value == [
            exp_point_3, exp_point_1, exp_point_2]

    def test_polynomial_coeff(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(1000, 5, 'lps')
        characteristic.add_point(3000, 61, 'lps')
        characteristic.add_point(2000, 25, 'lps')
        characteristic.add_point(7000, 485, 'lps')
        exp_coeffs = np.array([-5, 7, 2, 1])
        result = characteristic.polynomial_coeff(1)
        np.testing.assert_almost_equal(result, exp_coeffs)

    def test_polynomial_coeff_2_pumps(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(1000, 5, 'lps')
        characteristic.add_point(3000, 61, 'lps')
        characteristic.add_point(2000, 25, 'lps')
        characteristic.add_point(7000, 485, 'lps')
        exp_coeffs = np.array([-5, 3.5, 0.5, 0.125])
        result = characteristic.polynomial_coeff(2)
        np.testing.assert_almost_equal(result, exp_coeffs)

    def test_polynomial_coeff_3_pumps(self):
        characteristic = variables.PumpCharVariable()
        characteristic.add_point(1000, 5, 'lps')
        characteristic.add_point(3000, 61, 'lps')
        characteristic.add_point(2000, 25, 'lps')
        characteristic.add_point(7000, 485, 'lps')
        exp_coeffs = np.array([-5, 2.3333, 0.2222, 0.037037])
        result = characteristic.polynomial_coeff(3)
        np.testing.assert_almost_equal(result, exp_coeffs, decimal=4)
