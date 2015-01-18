import django
from django.core.urlresolvers import reverse
from django.test import override_settings

from kii.user.tests import base
from kii.tests import test_base_models


class TestViews(base.UserTestCase):
    
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
    
    def test_model_template_mixin_pass_context(self):
        response = self.client.get(reverse('kii:test_base_models:titlemodel2:list'))

        self.assertEqual(response.context['action'], "list")
        
        response = self.client.get(reverse('kii:test_base_models:titlemodel2:create'))
        self.assertEqual(response.context['action'], "create")

    
    def test_filters(self):

        i0 = self.G(test_base_models.models.StatusModel, status="pub")
        i1 = self.G(test_base_models.models.StatusModel, status="dra")
        i2 = self.G(test_base_models.models.StatusModel, status="pub")

        url = reverse('kii:test_base_models:statusmodel:list')
        response = self.client.get(url)

        self.assertQuerysetEqualIterable(response.context['object_list'], [i0, i1, i2], ordered=False)

        response = self.client.get(url+"?status=dra")

        self.assertQuerysetEqualIterable(response.context['object_list'], [i1], ordered=False)

        response = self.client.get(url+"?status=pub")

        self.assertQuerysetEqualIterable(response.context['object_list'], [i0, i2], ordered=False)

    def test_model_template_view_suffix_with_model_name(self):
        url = reverse('kii:test_base_models:statusmodel:list')

        response = self.client.get(url)
        self.assertIn("status model", response.context['full_title'])
