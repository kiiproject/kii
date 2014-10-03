from kii.app.tests import base
from kii.tests import test_base_models
import django
from django.core.urlresolvers import reverse


class TestViews(base.BaseTestCase):
    
    def test_model_template_mixin_automatically_find_templates(self):
        m = test_base_models.models.NameModel(name="hello")
        m.save()

        url = reverse("test_base_models:namemodel:detail", kwargs={'pk': m.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "test_base_models/namemodel/detail.html")
        