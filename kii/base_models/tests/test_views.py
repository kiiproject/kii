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
    
    def test_app_model_page_contains_model_verbose_name(self):

        response = self.client.get(reverse('kii:test_base_models:titlemodel:list'))
        parsed = self.parse_html(response.content)
        self.assertIn("Title Model", parsed.title.string)

    def test_model_template_mixin_pass_context(self):
        response = self.client.get(reverse('kii:test_base_models:titlemodel2:list'))

        self.assertEqual(response.context['action'], "list")
        
        response = self.client.get(reverse('kii:test_base_models:titlemodel2:create'))
        self.assertEqual(response.context['action'], "create")

    @override_settings(KII_DEFAULT_USER='test0')
    def test_owner_view_require_username_argument_or_deduce_it_automatically_from_logged_in_user_or_settings(self):
        url = reverse('kii:test_base_models:ownermodel:list')

        # anonymous user should see test0 page
        response = self.client.get(url)
        self.assertEqual(response.context['owner'], self.users[0])

        # authenticated user should see his own page
        re = self.login(self.users[1].username)
        print(re.content)
        response = self.client.get(url)
        self.assertEqual(response.context['owner'], self.users[1])

    def test_owner_view_raise_404_for_anonymous_user_without_KII_DEFAULT_USER_SET(self):
        url = reverse('kii:test_base_models:ownermodel:list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
