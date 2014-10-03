from . import base
from kii import stream


class TestStream(base.StreamTestCase):
    
    def test_new_user_gets_a_dedicated_stream(self):
        u = self.user_model(username="new_user")
        u.save()

        s = stream.models.Stream.objects.get(owner=u)

