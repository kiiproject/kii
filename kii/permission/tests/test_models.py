from kii.stream.tests import base
from kii.tests.test_permission import models
from kii import user
import django
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

    def test_can_assign_permission_to_group(self):
        m0 = G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm("read", self.all_users_group)

        self.assertEqual(m0.readable_by(self.users[1]), True)

    def test_allowing_premissions_to_anonymous_allow_to_everybody(self):
        m0 = G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm("read", self.anonymous_user)

        for user in self.user_model.objects.all():
            self.assertEqual(m0.readable_by(user), True)

    def test_allowing_all_users_group_does_not_allow_anonymous(self):
        m0 = G(models.PermissionModel, owner=self.users[0])
        m0.assign_perm("read", user.models.get_all_users_group())

        for u in self.user_model.objects.all().exclude(pk=self.anonymous_user.pk):
            self.assertEqual(m0.readable_by(u), True)

        self.assertEqual(m0.readable_by(self.anonymous_user), False)


class TestInheritPermissionMixin(base.StreamTestCase):

    def test_inheritopermissionmodel_inherit_root_owner(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m = G(models.InheritPermissionModel, root=p, inherit_permissions=True)

        self.assertEqual(m.owner, self.users[0])

    def test_inheritpermissionmodel_can_inherit_permissions(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m = G(models.InheritPermissionModel, root=p, inherit_permissions=True)

        self.assertEqual(m.readable_by(self.users[1]), False)
        p.assign_perm("read", self.users[1])

        self.assertEqual(m.readable_by(self.users[1]), True)

    def test_inheritpermissionqueryset_include_correct_objects(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m1 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)

        p.assign_perm("read", self.anonymous_user)

        readable = models.InheritPermissionModel.objects.all().readable_by(self.users[1])
        self.assertQuerysetEqualIterable(readable, [m1, m2], ordered=False)

    def test_inheritpermissionqueryset_include_all_owned_objects(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m1 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)

        readable = models.InheritPermissionModel.objects.all().readable_by(self.users[0])
        self.assertQuerysetEqualIterable(readable, [m1, m2, m3, m4], ordered=False)

    def test_inheritinheritpermissionmodel_can_inherit_permissions(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        i = G(models.InheritInheritPermissionModel, root=m, inherit_permissions=True)

        self.assertEqual(i.readable_by(self.users[1]), False)
        p.assign_perm("read", self.users[1])

        self.assertEqual(i.readable_by(self.users[1]), True)

    def test_inheritinheritpermissionqueryset_include_correct_objects(self):
        p = G(models.PermissionModel, owner=self.users[0])
        m1 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m2 = G(models.InheritPermissionModel, root=p, inherit_permissions=True)
        m3 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        m4 = G(models.InheritPermissionModel, root=p, inherit_permissions=False)
        i1 = G(models.InheritInheritPermissionModel, root=m1, inherit_permissions=True)
        i2 = G(models.InheritInheritPermissionModel, root=m2, inherit_permissions=False)
        i3 = G(models.InheritInheritPermissionModel, root=m3, inherit_permissions=True)
        i4 = G(models.InheritInheritPermissionModel, root=m4, inherit_permissions=False)

        p.assign_perm("read", self.anonymous_user)
        i4.assign_perm('read', self.users[1])
        readable = models.InheritInheritPermissionModel.objects.all().readable_by(self.users[1])
        self.assertQuerysetEqualIterable(readable, [i1, i4], ordered=False)

