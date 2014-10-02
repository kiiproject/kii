from stream.tests import base
from tests import test_base_models
import django
from guardian.shortcuts import assign

class TestUserPermission(base.StreamTestCase):
    
    def test_can_add_permission_to_stream(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("view", u2)
        
        self.assertEqual(stream.viewable(u2), True)
        self.assertEqual(stream.editable(u2), False)
        self.assertEqual(stream.deletable(u2), False)
            