import base
from ... import app
import apps
import models

class TestApp(base.BaseTestCase):

    def test_can_get_app_models(self):

        app = apps.test_app_1
        self.assertEqual(app.models.values(), [models.TestModel1, models.TestModel2])

    def test_can_get_apps(self):

        registry = app.registries.app_registry
        self.assertEqual(registry.values(), [apps.test_app_1, apps.test_app_2])