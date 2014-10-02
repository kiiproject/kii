from ... import app
import models
import django


class TestNameMixin(app.tests.base.BaseTestCase):

    
    def test_name_field(self):
        m = models.NameModel(name="Hello world!")
        m.save()
        
    def test_name_is_required(self):
        m = models.NameModel()

        with self.assertRaises(django.core.exceptions.ValidationError):
            m.save()