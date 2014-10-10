from kii.app.tests import base
from kii.tests import test_base_models
import django

class TestContentMixin(base.BaseTestCase):
    
    def test_get_renderered_field(self):

        m = self.G(test_base_models.models.ContentModel, content="#hello")
        self.assertEqual(m.content.rendered, "<h1>hello</h1>")


