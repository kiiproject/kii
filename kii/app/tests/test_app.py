from . import base
import app
from tests import test_app
from django.conf import settings
from django.apps import apps


class TestApp(base.BaseTestCase):

    def test_can_get_app_models(self):

        app = apps.get_app_config('test_app')

        expected_models = [test_app.models.TestModel1, test_app.models.TestModel2]
        i = 0
        for model in app.get_models():
            self.assertIn(model, expected_models)
            i += 1
        self.assertEqual(i, len(expected_models))    

    def test_kii_apps_are_registered(self):

        for a in settings.KII_APPS:
            self.assertEqual(True, apps.is_installed(a))