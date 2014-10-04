from kii.stream.tests import base
from kii.tests.test_permission import models
import django
from guardian.utils import get_anonymous_user
from django_dynamic_fixture import G


class TestPermissionMixin(base.StreamTestCase):

    def test_owner_can_view_permissionmodel(self):
        
        m = G(models.PermissionModel, owner=self.users[0])
        self.assertEqual(m.readable_by(self.users[0]), True)
        
    def test_permissionmodel_queryset_can_filter_instances_using_all_perms_level(self):
        m0 = G(models.PermissionModel, owner=self.users[0])
        m1 = G(models.PermissionModel, owner=self.users[0])
        m1.assign_perm("delete", self.users[1])
        m2 = G(models.PermissionModel, owner=self.users[0])
        
        user = self.users[1]
        queryset = models.PermissionModel.objects.readable_by(user)

        self.assertEqual(len(queryset), 1)
        self.assertIn(m1, queryset)

class TestPrivateViewMixin(base.StreamTestCase):
    
    def test_privateviewmixin_view_private_default_to_true(self):
        m = G(models.PrivateReadModel, owner=self.users[0])

        self.assertEqual(m.read_private, True)    

    def test_other_user_cannot_view_if_private_is_true(self):
        m = G(models.PrivateReadModel, owner=self.users[0])
        self.assertEqual(m.readable_by(self.users[1]), False)

    def test_other_user_can_see_if_private_is_false(self):
        m = G(models.PrivateReadModel, owner=self.users[0], read_private=False)
        self.assertEqual(m.readable_by(self.users[1]), True)
     
    def test_private_model_queryset_filter_private_instances_for_anonymous_users(self):
        m0 = G(models.PrivateReadModel, owner=self.users[0], read_private=True)
        m1 = G(models.PrivateReadModel, owner=self.users[0], read_private=False)
        
        user = get_anonymous_user()
        queryset = models.PrivateReadModel.objects.readable_by(user)

        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], m1)
        
    def test_private_model_queryset_can_private_instances_using_all_perms_level(self):
        m0 = G(models.PrivateReadModel, owner=self.users[0], read_private=True)
        m1 = G(models.PrivateReadModel, owner=self.users[0], read_private=True)
        m1.assign_perm("delete", self.users[1])
        m2 = G(models.PrivateReadModel, owner=self.users[0], read_private=False)
        
        user = self.users[1]
        queryset = models.PrivateReadModel.objects.readable_by(user)

        self.assertEqual(len(queryset), 2)
        self.assertIn(m1, queryset)
        self.assertIn(m2, queryset)

