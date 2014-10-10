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