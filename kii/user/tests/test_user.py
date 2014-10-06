from . import base
from ...tests import test_user
from django.contrib.auth.models import Group
from django.conf import settings

class TestUserData(base.UserTestCase):
    
    def test_users_are_added_to_default_group_on_creation(self):
        users = self.user_model.objects.all()
        all_users_group = Group.objects.get(name=settings.ALL_USERS_GROUP)
        self.assertEqual(len(users), len(all_users_group.user_set.all()))

        for u in users:
            self.assertIn(u, all_users_group.user_set.all())
        