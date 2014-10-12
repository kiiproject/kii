from . import base
from kii import stream
import django
from django.utils import timezone
from ...tests import test_stream


class TestStreamItem(base.StreamTestCase):
    
    def test_status_default_to_draft(self):

        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.status, "dra")

    def test_creation_and_modification_date(self):
        now = timezone.now()

        m = self.G(stream.models.StreamItem)
        self.assertEqual(m.created > now, True)
        self.assertEqual(m.last_modified > now, True)

    def test_permission_inheritance(self):
        m = self.G(stream.models.StreamItem, root=self.streams[0])

        u = self.users[1]
        self.assertEqual(m.readable_by(u), False)

        m.root.assign_perm('read', self.anonymous_user)
        self.assertEqual(m.readable_by(u), True)

        m.inherit_permissions = False
        m.save()

        self.assertEqual(m.readable_by(u), False)

        m.assign_perm('delete', u)

        self.assertEqual(m.readable_by(u), True)


    def test_polymorphic_integration(self):

        m1 = self.G(test_stream.models.StreamItemChild1, root=self.streams[0])
        m2 = self.G(test_stream.models.StreamItemChild2, root=self.streams[0])

        self.assertQuerysetEqualIterable(self.streams[0].children.all().select_subclasses(), [m1, m2], ordered=False)


