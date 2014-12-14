from kii.user.tests import base
from kii.tests import test_permission


class TestViews(base.UserTestCase):
    
    def test_permission_mixin_detail_view_is_accessible_by_owner(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])
        self.login(self.users[0])
        response = self.client.get(m.reverse('detail'))

        self.assertEqual(response.context['object'], m)

    def test_permission_mixin_detail_view_is_not_accessible_by_anonymous(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])

        response = self.client.get(m.reverse('detail'))
        self.assertEqual(response.status_code, 404)

    def test_permission_mixin_detail_view_is_accessible_by_authorized_user(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])
        m.assign_perm("read", self.users[1])
        self.login(self.users[1])

        response = self.client.get(m.reverse('detail'))
        self.assertEqual(response.context['object'], m)    
    
    def test_permission_mixin_update(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])
        m.assign_perm("write", self.users[1])
        self.login(self.users[1])

        response = self.client.get(m.reverse('update'))
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.context['object'], m)  

    def test_permission_mixin_delete(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])
        m.assign_perm("delete", self.users[1])
        self.login(self.users[1])

        response = self.client.get(m.reverse('delete'))
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.context['object'], m) 

    def test_permission_mixin_return_404_if_user_has_no_required_perm(self):
        m = self.G(test_permission.models.PermissionModel, owner=self.users[0])
        self.login(self.users[1])

        response = self.client.get(m.reverse('delete'))
        self.assertEqual(response.status_code, 404)