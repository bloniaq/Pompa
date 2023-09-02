import pompa.models.pumpsystem
from pompa.exceptions import ErrorContainer, WellTooSmallError,\
    InletInDeadVolumeError, InsidePipesTooShortError


def test_WellTooSmallError(app_fixture):
    with app_fixture as app:
        filepath = 'tests/scenarios/09-5_pomp_max_doplyw_kres_wydajności.DAN'
        app.load_file(filepath, 'lps')
        s = app.model
        s.safety.set('economic')
        pompa.models.pumpsystem.PumpSystem(s)
        error_container = ErrorContainer()
        assert error_container.get_errors() == []

        s.safety.set('optimal')
        pompa.models.pumpsystem.PumpSystem(s)
        if not error_container.get_errors(): assert False
        for error in error_container.get_errors():
            if isinstance(error, WellTooSmallError):
                break
            else:
                assert False

def test_InletInDeadVolume(app_fixture):
    with app_fixture as app:
        filepath = 'tests/scenarios/13-doplyw_ponizej_martwej_objetosci.DAN'
        app.load_file(filepath, 'lps')
        s = app.model
        pompa.models.pumpsystem.PumpSystem(s)
        error_container = ErrorContainer()
        if not error_container.get_errors():
            assert False
        for error in error_container.get_errors():
            if isinstance(error, InletInDeadVolumeError):
                break
            else:
                assert False

def test_InsidePipesTooShortError(app_fixture):
    with app_fixture as app:
        filepath = 'tests/scenarios/14-za_krotki_przewod_wewn.DAN'
        app.load_file(filepath, 'lps')
        s = app.model
        ps = pompa.models.pumpsystem.PumpSystem(s)
        error_container = ps.error_container
        print(error_container.get_errors())
        if not error_container.get_errors():
            assert False
        for error in error_container.get_errors():
            if isinstance(error, InsidePipesTooShortError):
                break
            else:
                assert False
