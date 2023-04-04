import pytest
import numpy as np
import tkinter as tk
import pompa.view.figures as figs


class TestPumpGraph:

    @pytest.fixture(scope="function")
    def root_frame(self, request):
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()
        yield root, frame
        root.destroy()

    @pytest.fixture
    def data_full_1(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 19, 20, 21, 25],
                           [19.6, 19.6, 17.2, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.24929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (15, 19),
        }
        return data

    @pytest.fixture
    def data_full_1_diff_x(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6.2, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 19, 20, 21, 25],
                           [19.6, 19.6, 17.2, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.24929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (15, 19),
        }
        return data

    @pytest.fixture
    def data_full_1_diff_point(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 19, 20, 21, 25],
                           [19.6, 19.6, 17.1, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.24929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (15, 19),
        }
        return data

    @pytest.fixture
    def data_full_1_diff_poly(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 19, 20, 21, 25],
                           [19.6, 19.6, 17.2, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.23929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (15, 19),
        }
        return data

    @pytest.fixture
    def data_full_1_diff_eff(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 19, 20, 21, 25],
                           [19.6, 19.6, 17.2, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.24929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (14.9, 19),
        }
        return data

    @pytest.fixture
    def data_full_1_del_point(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 20, 21, 25],
                           [19.6, 19.6, 16.6, 15, 7.5]),
            'y_p_char': np.polynomial.Polynomial(
                [-5.24929846e-01, 2.92517759e+03, -1.04118507e+05]),
            'y_p_eff': (14.9, 19),
        }
        return data

    @pytest.fixture
    def data_empty(self):
        data = {
            'x': None,
            'y_p_points': None,
            'y_p_char': None,
            'y_p_eff': None,
        }
        return data\

    @pytest.fixture
    def data_x_and_points(self):
        data = {
            'x': np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            'y_p_points': ([6, 12, 21, 25],
                           [19.6, 19.6, 15, 7.5]),
            'y_p_char': None,
            'y_p_eff': None,
        }
        return data

    def test_same_data_same_data(self, data_full_1, root_frame):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert pump_graph._same_data(data_full_1, data_full_1)

    def test_same_data_diff_x(self, root_frame, data_full_1,
                              data_full_1_diff_x):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_full_1_diff_x)

    def test_same_data_diff_point(self, root_frame, data_full_1,
                                  data_full_1_diff_point):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_full_1_diff_point)

    def test_same_data_diff_poly(self, root_frame, data_full_1,
                                 data_full_1_diff_poly):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_full_1_diff_poly)

    def test_same_data_diff_eff(self, root_frame, data_full_1,
                                data_full_1_diff_eff):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_full_1_diff_eff)

    def test_same_data_full_vs_empty(self, root_frame, data_full_1, data_empty):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_empty)

    def test_same_data_empty_vs_full(self, root_frame, data_full_1, data_empty):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_empty, data_full_1)

    def test_same_data_del_point(self, root_frame, data_full_1,
                                 data_full_1_del_point):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_full_1, data_full_1_del_point)

    def test_same_data_empty_vs_empty(self, root_frame, data_empty):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert pump_graph._same_data(data_empty, data_empty)

    def test_same_data_empty_vs_half_empty(self, root_frame, data_empty,
                                           data_x_and_points):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_x_and_points, data_empty)

    def test_same_half_empty_vs_empty(self, root_frame, data_empty,
                                      data_x_and_points):
        pump_graph = figs.PumpGraph(root_frame[1])
        assert not pump_graph._same_data(data_empty, data_x_and_points)
