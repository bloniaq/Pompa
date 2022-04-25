import pompa.application as pompa
import pompa.view as view

class Test_Application:

    def test_app_init(self):
        with pompa.Application() as app:
            assert isinstance(app, pompa.Application)

    def test_gui_tkinter(self):
        with pompa.Application() as app:
            assert isinstance(app.view, view.gui_tk.View)

    def test_get_var(self):
        with pompa.Application() as app:
            test_name = 'ord_terrain'
            for var in app.variables:
                if var.name is test_name:
                    test_var = var

        assert app.get_var(test_name) == test_var

    def test_binding_m_and_v_vars(self):
        with pompa.Application() as app:
            assert app.get_var('ord_terrain').viewvar is app.view.vars['ord_terrain']
            assert app.get_var('ord_terrain').modelvar is app.model.get_var('ord_terrain')
