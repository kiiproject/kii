from kii.app.tests import base
from kii.tests import test_base_models
import django


class TestNameMixin(base.BaseTestCase):

    
    def test_name_field(self):
        m = test_base_models.models.NameModel(name="Hello world!")
        m.save()
        
    def test_name_is_required(self):
        m = test_base_models.models.NameModel()

        with self.assertRaises(django.core.exceptions.ValidationError):
            m.save()