import django

from kii.app.tests import base
from kii.tests import test_base_models
from kii.tests.test_base_models import forms

class TestContentMixin(base.BaseTestCase):
    
    def test_get_renderered_field(self):

        m = self.G(test_base_models.models.ContentModel, content="#hello")
        self.assertEqual(m.content.rendered, "<h1>hello</h1>")

    def test_raw_field(self):
        m = self.G(test_base_models.models.ContentModel, content="#hello")
        self.assertEqual(m.content.raw, "#hello")


class TestContentMixinForm(base.BaseTestCase):
    
    def test_form(self):
        form_data = {'content': 'test'}
        form = forms.ContentModelForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
