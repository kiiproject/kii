from . import base
from kii import stream
import django
from django.utils import timezone

class TestStreamItem(base.StreamTestCase):
    
    def test_requires_a_stream(self):
        i = stream.models.StreamItem(title='1')

        with self.assertRaises(django.db.IntegrityError):
            i.save()   

    def test_status_default_to_draft(self):

        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.status, "dra")

    def test_creation_and_modification_date(self):
        now = timezone.now()

        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.creation_date > now, True)
        self.assertEqual(m.last_modification_date > now, True)