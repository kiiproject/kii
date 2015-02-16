import django

from kii.app.tests import base
from kii.tests import test_base_models
from ..forms import TitleMixinForm

class TestImportanceMixin(base.BaseTestCase):

    
    def test_name_field(self):
        m = self.G(test_base_models.models.ImportanceModel)
        self.assertEqual(m.importance, 2)
        


