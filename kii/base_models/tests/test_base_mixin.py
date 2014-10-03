from kii.app.tests import base
from kii.tests import test_base_models
import django


class TestBaseMixin(base.BaseTestCase):
    
    def test_can_get_url_namespace(self):
        m = test_base_models.models.NameModel(name="Hello world!")
        m.save()

        self.assertEqual(m.url_namespace, "test_base_models:namemodel:")

        