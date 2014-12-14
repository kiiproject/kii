from django.core.urlresolvers import reverse

from . import base
from kii import stream


class TestStream(base.StreamTestCase):
    
    def test_new_user_gets_a_dedicated_stream(self):
        u = self.user_model(username="new_user")
        u.save()

        s = stream.models.Stream.objects.get(owner=u)

    def test_default_user_stream_is_titled_with_owner_username(self):

        u = self.user_model(username="this_is_my_username")
        u.save()

        s = stream.models.Stream.objects.get(title="this_is_my_username")
        self.assertEqual(s.owner, u)

    def test_can_update_stream(self):
        url = reverse("kii:stream:stream:update")
        self.login(self.users[0].username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].title, "test0")