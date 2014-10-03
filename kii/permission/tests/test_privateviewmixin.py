from kii.stream.tests import base
from kii.tests.test_permission import models
import django

class TestUserPermission(base.StreamTestCase):
    
    def test_privateviewmixin_view_private_default_to_true(self):
        m = models.PrivateViewModel(owner=self.users[0])
        m.save()

        self.assertEqual(m.view_private, True)

    def test_owner_can_view_privateviewmixin(self):
        
        m = models.PrivateViewModel(owner=self.users[0])
        m.save()
        self.assertEqual(m.viewable(self.users[0]), True)

    def test_other_user_cannot_view_if_private_is_true(self):
        m = models.PrivateViewModel(owner=self.users[0])
        m.save()
        self.assertEqual(m.viewable(self.users[1]), False)

    def test_other_user_can_see_if_private_is_false(self):
        m = models.PrivateViewModel(owner=self.users[0], view_private=False)
        m.save()
        self.assertEqual(m.viewable(self.users[1]), True)

     
