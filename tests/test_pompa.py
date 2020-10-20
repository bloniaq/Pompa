import pompa

def test_app_init():

    app = pompa.Application()

    assert isinstance(app, pompa.Application)
