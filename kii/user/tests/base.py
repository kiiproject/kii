import django
from django.conf import settings
from django.contrib.auth.models import Group
from guardian.utils import get_anonymous_user
from django.core.urlresolvers import reverse
from ...app.tests import base


class UserTestCase(base.BaseTestCase):

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()
        super(UserTestCase, self).setUp()
        
        self.users = {
            0: self.user_model(username="test0"),
            1: self.user_model(username="test1"),
            2: self.user_model(username="test2"),
        }
        for key, user in self.users.items():
            user.set_password('test')
            user.save()

        self.all_users_group = Group.objects.get(name=settings.ALL_USERS_GROUP)
        self.anonymous_user = get_anonymous_user()

    def login(self, username, password="test"):
        return self.client.post(reverse(settings.LOGIN_URL), {"username": username, "password": password})

    def logout(self):
        return self.client.get(settings.LOGOUT_URL)

    def tearDown(self):
        self.logout()

    def assertRedirectsLogin(self, response, next):
        self.assertRedirects(response, reverse(settings.LOGIN_URL)+"?next="+next)