from . import base
import stream
import django


class TestStreamItem(base.StreamTestCase):
    
    def test_stream_item_requires_a_stream(self):
        i = stream.models.StreamItem(name='1')

        with self.assertRaises(django.db.IntegrityError):
            i.save()   
