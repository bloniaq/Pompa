import pompa.application as app_module
import pompa.view.gui_tk as view_module


class TestView:

    def test_init(self, mocked_vm_variables_data):
        with view_module.View(mocked_vm_variables_data) as view:
            # testing variables creating
            assert 'mode' in view.vars.keys()
            # testing default values setting
            assert view.vars['shape'].get() == 'round'
