import django
from guardian.shortcuts import assign
from guardian.models import UserObjectPermission

from kii.stream.tests import base
from kii.tests import test_base_models
from .. import forms

class TestUserPermission(base.StreamTestCase):
    
    def test_view_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("read", u2)

        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), False)
        self.assertEqual(stream.deletable_by(u2), False)
            
    def test_edit_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("write", u2)

        # should return True for read and write
        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), True)
        self.assertEqual(stream.deletable_by(u2), False)
            
    def test_remove_permission(self):
        u2 = self.users[2]
        stream = self.streams[0]
        stream.assign_perm("delete", u2)

        # should return True for read, write and delete
        self.assertEqual(stream.readable_by(u2), True)
        self.assertEqual(stream.writable_by(u2), True)
        self.assertEqual(stream.deletable_by(u2), True)

    def test_can_remove_permission(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)
        self.assertEqual(i.readable_by(self.anonymous_user), True)

        i.remove_perm('read', self.anonymous_user)
        self.assertEqual(i.readable_by(self.anonymous_user), False)

    def test_owner_gets_all_permissions(self):
        stream = self.streams[0]
        self.assertEqual(stream.deletable_by(stream.owner), True)
        
    def test_permission_is_deleted_when_stream_is_deleted(self):
        u2 = self.users[2]
        stream = self.streams[0]
        perm = stream.assign_perm("delete", u2)
        u2.delete()

        with self.assertRaises(UserObjectPermission.DoesNotExist):
            UserObjectPermission.objects.get(pk=perm.pk)

    def test_permission_mixin_form_populate_fields_correctly(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)

        form = forms.PermissionMixinForm(instance=i)
        self.assertEqual(form.fields['readable_by'].initial, "everybody")

    def test_permission_mixin_form__save_create_permission(self):
        i = self.streams[0]
        form = forms.PermissionMixinForm(data={'readable_by': "everybody"}, instance=i)

        self.assertEqual(form.is_valid(), True)

        form.save()

        self.assertEqual(i.readable_by(self.anonymous_user), True)

    def test_permission_mixin_form_delete_obsolete_permission(self):
        i = self.streams[0]
        i.assign_perm('read', self.anonymous_user)
        form = forms.PermissionMixinForm(data={'readable_by': "owner"}, instance=i)

        self.assertEqual(form.is_valid(), True)

        form.save()

        self.assertEqual(i.readable_by(self.anonymous_user), False)