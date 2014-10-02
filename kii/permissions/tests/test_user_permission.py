from stream.tests import base
from tests import test_base_models
import django
from guardian.shortcuts import assign
from guardian.models import UserObjectPermission

class TestUserPermission(base.StreamTestCase):
    
    def test_view_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("view", u2)

        self.assertEqual(stream.viewable(u2), True)
        self.assertEqual(stream.editable(u2), False)
        self.assertEqual(stream.deletable(u2), False)
            
    def test_edit_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("edit", u2)

        # should return True for view and edit
        self.assertEqual(stream.viewable(u2), True)
        self.assertEqual(stream.editable(u2), True)
        self.assertEqual(stream.deletable(u2), False)
            
    def test_delete_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("delete", u2)

        # should return True for view, edit and delete
        self.assertEqual(stream.viewable(u2), True)
        self.assertEqual(stream.editable(u2), True)
        self.assertEqual(stream.deletable(u2), True)

    def test_owner_gets_all_permissions(self):
        stream = self.streams[0]
        self.assertEqual(stream.deletable(stream.owner), True)
        
    def test_permission_is_deleted_when_stream_is_deleted(self):
        u2 = self.users[2]
        stream = self.streams[0]
        perm = stream.assign_perm("delete", u2)
        u2.delete()

        with self.assertRaises(UserObjectPermission.DoesNotExist):
            UserObjectPermission.objects.get(pk=perm.pk)

