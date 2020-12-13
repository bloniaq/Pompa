import pompa.models.variables as variables
import numpy as np


class Test_PumpCharVar:
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
