from kii.app.tests import base
from kii.tests import test_base_models
import django


class TestBaseMixin(base.BaseTestCase):
    
    def test_can_get_url_namespace(self):
        m = test_base_models.models.NameModel(name="Hello world!")
        m.save()

        self.assertEqual(m.url_namespace, "kii:test_base_models:namemodel:")

    def test_model_reverse(self):
        m = test_base_models.models.NameModel(name="Hello world!")
        m.save()
        self.assertEqual(m.reverse('detail'), "/kii/test_base_models/namemodel/{0}/".format(m.pk))
        self.assertEqual(m.reverse('list'), "/kii/test_base_models/namemodel/")

    def test_model_class_reverse(self):
        m = test_base_models.models.NameModel
        self.assertEqual(m.class_reverse('list'), "/kii/test_base_models/namemodel/")