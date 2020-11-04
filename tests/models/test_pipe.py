import pytest
import pompa.models.pipe as pipe


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


@pytest.mark.parametrize('roughness, diameter, result', [
    (0.001, 0.1, 0.01),
    (0.0015, 0.1, 0.015)])
def test_epsilon(roughness, diameter, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.roughness.set(roughness)
    pipe_obj.diameter.set(diameter)
    assert pipe_obj._epsilon() == result


@pytest.mark.parametrize('diameter, flow, result', [
    (0.09978, 1, 0.0352),
    (0.125, 0.99, 0.0224),
    (0.31000001, 1.36889, 0.005),
    (0.075, 2.54877, 0.1610),
    (0.090, 1.45, 0.0629),
    (0.125, 145, 3.2746),
    (0.125, 94.78, 2.1405)])
def test_speed(diameter, flow, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(diameter)
    flow_var = pipe.v.FlowVariable(flow)
    assert pipe_obj._speed(flow_var) == result


@pytest.mark.parametrize('diameter, flow, result', [
    (0.125, 95, 266364),
    (0.200, 135.894, 238796),
    (0.250, 150, 210717),
    (0.300, 12.45, 14571)])
def test_reynolds_n(diameter, flow, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(diameter)
    flow_var = pipe.v.FlowVariable(flow)
    assert pipe_obj._reynolds_n(flow_var) == result


@pytest.mark.parametrize('_lambda, epsilon, result', [
    (0.03, 0.01, 115470),
    (0.0379, 0.01, 102733)])
def test_boundary_reynolds_n(_lambda, epsilon, result):
    pipe_obj = pipe.Pipe()

    def fake_epsilon():
        return epsilon

    pipe_obj._epsilon = fake_epsilon

    assert pipe_obj._boundary_reynolds_n(_lambda) == result


@pytest.mark.parametrize('reynolds_n, epsilon, result', [
    (189792, 0.01, 0.0382)])
def test_boundary_lambda(reynolds_n, epsilon, result):
    pipe_obj = pipe.Pipe()

    def fake_epsilon():
        return epsilon

    pipe_obj._epsilon = fake_epsilon

    assert pipe_obj._boundary_lambda(reynolds_n) == result


@pytest.mark.parametrize('reynolds_n, epsilon, result', [
    (0, 0, 0),
    (128, 0, 0.5),
    (2500, 0, 0),
    (6000, 0, 0.0359),
    (9000, 0, 0.0325),
    (90000, 0, 0.0183),
    (101000, 0.009, 0.0373),
    (189792, 0.01, 0.0379)])
def test_lambda(reynolds_n, epsilon, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.diameter.set(0.100)
    pipe_obj.roughness.set(0.001)

    def fake_epsilon():
        return epsilon

    pipe_obj._epsilon = fake_epsilon

    assert pipe_obj._lambda(reynolds_n) == result


@pytest.mark.parametrize('length, diameter, roughness, result', [
    (1.5, 0.1, 0.001, 0.104),
    (50, 0.11, 0.0015, 2.437)])
def test_line_loss(length, diameter, roughness, result):
    pipe_obj = pipe.Pipe()
    flow = pipe.v.FlowVariable(15, 'lps')
    pipe_obj.diameter.set(diameter)
    pipe_obj.roughness.set(roughness)
    pipe_obj.length.set(length)
    assert pipe_obj._line_loss(flow) == result


@pytest.mark.parametrize('speed, loc_resists, result', [
    (1.91, [0.3, 0.5, 0.2, 0.1], 0.20),
    (1.58, [0.1, 0.1, 0.2], 0.05)])
def test_local_loss(speed, loc_resists, result):
    pipe_obj = pipe.Pipe()
    pipe_obj.resistance.set(loc_resists)
    _ = 0

    def fake_speed(_):
        return speed

    pipe_obj._speed = fake_speed
    assert pipe_obj._local_loss(_) == result
