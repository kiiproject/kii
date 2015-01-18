from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from kii.stream.tests import base
from kii.user import get_kii_users_group


class GlueViewsTestCase(base.StreamTestCase):

    def test_home_has_correct_context(self):

        url = reverse('kii:glue:home')
        response = self.client.get(url)

        self.assertQuerysetEqualIterable(response.context['kii_users'].all(),
                                         [user for key, user in self.users.items()])

    def test_base_template_includes_tracking_code(self):
        url = reverse('kii:glue:home')
        tracking_code = "<script>Test tracking</script>"
        with self.settings(TRACKING_CODE=tracking_code):
            response = self.client.get(url)
        self.assertIn(tracking_code.encode("utf-8"), response.content)




