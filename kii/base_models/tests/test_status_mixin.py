from kii.app.tests import base
from kii.tests import test_base_models
import django
from django.utils import timezone

class TestStatusMixin(base.BaseTestCase):

    
    def test_setting_status_to_published_set_publication_date(self):

        m = self.G(test_base_models.models.StatusModel)

        self.assertEqual(m.publication_date, None)

        now = timezone.now()
        m.status = "pub"
        m.save()

        self.assertEqual(m.publication_date > now, True)

