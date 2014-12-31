from django.core.urlresolvers import reverse

from kii.stream.tests import base
from kii.user import get_kii_users_group


class GlueViewsTestCase(base.StreamTestCase):

    def test_home_has_correct_context(self):

        url = reverse('kii:index')
        response = self.client.get(url)

        self.assertQuerysetEqualIterable(response.context['kii_users'].all(),
                                         [user for key, user in self.users.items()])





