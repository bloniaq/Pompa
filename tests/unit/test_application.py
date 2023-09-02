import pompa.application as pompa
import pompa.view as view


class TestVMVar:

    def test_instance_init(self):
        test_name = "variable"
        test_id = 0
        test_def_value = 5.45

        var = pompa.VMVar(test_name, test_id, test_def_value)

        assert var.name == test_name
        assert var.id == test_id
        assert var.default_value == test_def_value
        assert var.viewvar is None
        assert var.modelvar is None


class TestApplication:

    def test_app_init(self, app_fixture):
        with app_fixture as app:
            assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self, app_fixture):
        with app_fixture as app:
            assert isinstance(app.view, view.gui_tk.View)
