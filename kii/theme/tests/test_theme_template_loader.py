from kii.app.tests import base
from .. import loaders
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

class TestThemeTemplateLoader(base.BaseTestCase):

    def test_loader_prefix_themepath_with_theme_name(self):
        loader = loaders.ThemeLoader()
        template, something = loader("test_theme/test0.html")
        self.assertEqual(template.render(Context()), "Hello world!")

    def test_load_theme_template_first(self):
        # this template exists in default theme
        template = get_template("test_theme/test0.html")
        self.assertEqual(template.render(Context()), "Hello world!")

        # this one does not
        template = get_template("test_theme/test1.html")
        self.assertEqual(template.render(Context()), "Hello world!")
