from kii.app.tests import base
from kii.tests import test_base_models
import django


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
        print(url, m.url_namespace)
        response = self.client.get(url)
        parsed = self.parse_html(response.content)
        self.assertIn("Hello world!", parsed.title.string)
        
