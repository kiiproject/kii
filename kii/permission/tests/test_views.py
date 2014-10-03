from kii.user.tests import base
from kii.tests import test_permission
import django
from django.core.urlresolvers import reverse


class TestViews(base.UserTestCase):
    
    def test_private_model_detail_view_is_accessible_by_owner(self):
        m = test_permission.models.PrivateReadModel(owner=self.users[0])
        m.save()
        self.login(self.users[0])
        url = reverse("test_permission:privatereadmodel:detail", kwargs={'pk': m.pk})
        response = self.client.get(url)

        self.assertEqual(response.context['object'], m)

    def test_private_model_detail_view_is_not_accessible_by_anonymous(self):
        m = test_permission.models.PrivateReadModel(owner=self.users[0], read_private=True)
        m.save()
        url = reverse("test_permission:privatereadmodel:detail", kwargs={'pk': m.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_private_model_detail_view_is_accessible_by_authorized_user(self):
        m = test_permission.models.PrivateReadModel(owner=self.users[0], read_private=True)
        m.save()
        m.assign_perm("read", self.users[1])
        self.login(self.users[1])
        url = reverse("test_permission:privatereadmodel:detail", kwargs={'pk': m.pk})

        response = self.client.get(url)
        self.assertEqual(response.context['object'], m)
        
