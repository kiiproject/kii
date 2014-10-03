from ...app.tests import base
import django
from django.conf import settings

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

    def login(self, username, password="test"):
        return self.client.post(settings.LOGIN_URL, {"username": username, "password": password})

    def logout(self):
        return self.client.get(settings.LOGOUT_URL)

    def tearDown(self):
        self.logout()