import django

from kii.app.tests import base
from kii.tests import test_base_models
from ..forms import TitleMixinForm

class TestTitleMixin(base.BaseTestCase):

    
    def test_name_field(self):
        m = test_base_models.models.TitleModel(title="Hello world!")
        m.save()
        
    def test_name_is_required(self):
        m = test_base_models.models.TitleModel()

        with self.assertRaises(django.core.exceptions.ValidationError):
            m.save()


class TestTitleMixinView(base.BaseTestCase):

    
    def test_detail_title_mixin_sets_page_title_to_model_title(self):
        m = self.G(test_base_models.models.TitleModel, title="Hello world!")
        url = m.reverse('detail')
        response = self.client.get(url)
        parsed = self.parse_html(response.content)
        self.assertIn("Hello world!", parsed.title.string)
        


class TestTitleMixinForm(base.BaseTestCase):
    
    def test_form(self):
        form_data = {'title': 'test'}
        form = TitleMixinForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_form_empty_title_not_allowed(self):
        form_data = {'title': ''}
        form = TitleMixinForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
        
