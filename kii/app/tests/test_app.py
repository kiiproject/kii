from . import base
from kii import app
from kii.tests.test_app import apps as test_apps, models
from django.conf import settings
from django.apps import apps as django_app_registry
from ..core import apps
from django.core.urlresolvers import reverse


class TestApp(base.BaseTestCase):


    def test_can_get_app(self):
        app = apps.get('test_app')
        self.assertEqual(isinstance(app, test_apps.App), True)

    def test_can_get_all_apps(self):
        all_apps = list(apps.all())
        django_apps = list(django_app_registry.get_app_configs())
        self.assertEqual(django_apps, all_apps)  

    def test_can_get_kii_app(self):
        kii_apps = apps.kii_apps()  
        self.assertEqual(len(kii_apps), len(settings.KII_APPS + settings.TEST_APPS))
        for app in kii_apps:
            self.assertIn(app.name, settings.KII_APPS + settings.TEST_APPS)

    def test_kii_apps_are_registered(self):
        for a in settings.KII_APPS:
            self.assertEqual(True, django_app_registry.is_installed(a))

    def test_kii_app_installed_property(self):

        for app in apps.kii_apps():
            self.assertEqual(app.installed, True)

    def test_can_gather_urls_for_kii_apps(self):
        reverse('kii:test_app:index')
        reverse('kii:test_app1:some_view')
        reverse('kii:test_app2:third_view')


    def test_app_templates_inherit_from_page_template(self):
        response = self.client.get(reverse('kii:test_app:home'))
        self.assertTemplateUsed(response, "app/app_page.html")
        self.assertTemplateUsed(response, "app/base.html")

    def test_app_pages_title_contains_app_verbose_name(self):
        response = self.client.get(reverse('kii:test_app:home'))
        parsed = self.parse_html(response.content)
        self.assertIn("Test app", parsed.title.string)
