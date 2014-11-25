from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import os

from kii.app.tests import base
from kii.tests import test_theme
from .. import finders



class TestStaticThemeLoader(base.BaseTestCase):

    def test_theme_loader_return_files_prefixed_with_theme_name_if_they_exists(self):
        finder = finders.ThemeFinder()
        result = finder.find('test_theme/default.txt')
        expected_path = os.path.join(os.path.dirname(test_theme.__file__), 'static', 'default', 'test_theme', 'default.txt')
        self.assertEqual(result, expected_path)
