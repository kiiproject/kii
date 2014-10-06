from . import base
from ...tests import test_user
from django.contrib.auth.models import Group
from django.conf import settings


class TestUserData(base.UserTestCase):
    
    def test_users_are_added_to_default_group_on_creation_except_anonymous_user(self):
        users = self.user_model.objects.all().exclude(pk=self.anonymous_user.pk)
        self.assertEqual(len(users), len(self.all_users_group.user_set.all()))

        for u in users:
            self.assertIn(u, self.all_users_group.user_set.all())
        
        self.assertNotIn(self.anonymous_user, self.all_users_group.user_set.all())