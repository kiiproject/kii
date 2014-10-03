from kii.user.tests import base
from kii.tests import test_permission
import django
from django.core.urlresolvers import reverse
from django_dynamic_fixture import G

class TestViews(base.UserTestCase):
    
    def test_private_model_detail_view_is_accessible_by_owner(self):
        m = G(test_permission.models.PrivateReadModel, owner=self.users[0], read_private=True)
        self.login(self.users[0])
        response = self.client.get(m.reverse('detail'))

        self.assertEqual(response.context['object'], m)

    def test_private_model_detail_view_is_not_accessible_by_anonymous(self):
        m = G(test_permission.models.PrivateReadModel, owner=self.users[0], read_private=True)

        response = self.client.get(m.reverse('detail'))
        self.assertEqual(response.status_code, 404)

    def test_private_model_detail_view_is_accessible_by_authorized_user(self):
        m = G(test_permission.models.PrivateReadModel, owner=self.users[0], read_private=True)
        m.assign_perm("read", self.users[1])
        self.login(self.users[1])

        response = self.client.get(m.reverse('detail'))
        self.assertEqual(response.context['object'], m)        

    def test_private_model_list_filter_private_instances_for_anonymous_users(self):
        m0 = G(test_permission.models.PrivateReadModel, owner=self.users[0], read_private=True)
        m1 = G(test_permission.models.PrivateReadModel, owner=self.users[0], read_private=False)
        response = self.client.get(m0.reverse('list'))

        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0], m1)

