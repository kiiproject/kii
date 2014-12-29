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
        response = self.client.get(url)
        self.assertEqual(response.context['owner'], self.users[1])

    def test_owner_view_redirect_to_login_for_anonymous_user_without_KII_DEFAULT_USER_SET(self):
        url = reverse('kii:test_base_models:ownermodel:list')

        response = self.client.get(url)
        self.assertRedirects(response, reverse("kii:user:login")+"?next="+url)

    
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
        self.assertIn("status model", response.context['page_title'])

    def test_owner_middleware_with_kwarg(self):
        url = reverse('kii:user_area:test_base_models:ownermodel:list', kwargs={"username": self.users[0]})
        
        response = self.client.get(url)

        self.assertEqual(response.context['request'].owner, self.users[0])
        self.assertEqual(response.status_code, 200)

    def test_owner_middleware_with_logger_in_user(self):
        url = reverse('kii:test_base_models:ownermodel:list')
        self.login(self.users[1])
        response = self.client.get(url)

        self.assertEqual(response.context['request'].owner, self.users[1])
        self.assertEqual(response.status_code, 200)

    @override_settings(KII_DEFAULT_USER='test0')
    def test_owner_middleware_with_default_user(self):
        url = reverse('kii:test_base_models:ownermodel:list')
        response = self.client.get(url)

        self.assertEqual(response.context['request'].owner, self.user_model.objects.get(username='test0'))
        self.assertEqual(response.status_code, 200)
