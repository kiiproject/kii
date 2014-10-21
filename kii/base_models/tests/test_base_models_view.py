from kii.app.tests import base
from kii.tests import test_base_models
import django
from django.core.urlresolvers import reverse


class TestViews(base.BaseTestCase):
    
    def test_model_template_mixin_automatically_find_templates(self):
        m = self.G(test_base_models.models.TitleModel, title="hello")

        url = reverse("kii:test_base_models:titlemodel:detail", kwargs={'pk': m.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "test_base_models/titlemodel/detail.html")

    def test_model_template_mixin_uses_parent_class_template_if_none_found(self):
        m = self.G(test_base_models.models.TitleModel2, title="hello")

        url = reverse("kii:test_base_models:titlemodel2:detail", kwargs={'pk': m.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "test_base_models/titlemodel/detail.html")

        