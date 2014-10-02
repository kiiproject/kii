import base
import app
from tests import test_app

class TestApp(base.BaseTestCase):

    def test_can_get_app_models(self):

        app = test_app.apps.test_app_1
        self.assertEqual(app.models.values(), [test_app.models.TestModel1, test_app.models.TestModel2])

    def test_can_get_apps(self):

        registry = app.registries.app_registry
        self.assertEqual(registry.values(), [test_app.apps.test_app_1, test_app.apps.test_app_2])