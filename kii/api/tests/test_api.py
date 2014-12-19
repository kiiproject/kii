from kii.app.tests import base
from django.core.urlresolvers import reverse


class TestBaseMixin(base.BaseTestCase):
    
    def test_can_collect_api_views(self):

        reverse("kii:api:test_api0:index")
        reverse("kii:api:test_api1:index")