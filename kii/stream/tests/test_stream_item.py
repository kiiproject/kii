from . import base
from kii import stream
import django


class TestStreamItem(base.StreamTestCase):
    
    def test_stream_item_requires_a_stream(self):
        i = stream.models.StreamItem(title='1')

        with self.assertRaises(django.db.IntegrityError):
            i.save()   

    def test_stream_item_status_default_to_draft(self):

        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.status, "dra")