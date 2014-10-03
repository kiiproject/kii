from kii.stream.tests import base
from kii.tests.test_permission import models
import django

class TestPrivateViewMixin(base.StreamTestCase):
    
    def test_privateviewmixin_view_private_default_to_true(self):
        m = models.PrivateReadModel(owner=self.users[0])
        m.save()

        self.assertEqual(m.read_private, True)

    def test_owner_can_view_privateviewmixin(self):
        
        m = models.PrivateReadModel(owner=self.users[0])
        m.save()
        self.assertEqual(m.readable(self.users[0]), True)

    def test_other_user_cannot_view_if_private_is_true(self):
        m = models.PrivateReadModel(owner=self.users[0])
        m.save()
        self.assertEqual(m.readable(self.users[1]), False)

    def test_other_user_can_see_if_private_is_false(self):
        m = models.PrivateReadModel(owner=self.users[0], read_private=False)
        m.save()
        self.assertEqual(m.readable(self.users[1]), True)

     

