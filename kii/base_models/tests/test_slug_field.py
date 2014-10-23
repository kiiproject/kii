from __future__ import unicode_literals
from kii.app.tests import base
from kii.tests import test_base_models
import django

class TestSlugField(base.BaseTestCase):
    
    def test_can_set_slug_from_other_field(self):

        m = self.G(test_base_models.models.SlugModel, title="This is my title")
        self.assertEqual(m.slug, "this-is-my-title")

