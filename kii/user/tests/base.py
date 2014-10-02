import app
import django


class UserTestCase(app.tests.base.BaseTestCase):

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()
        super(UserTestCase, self).setUp()
        
        self.users = {
            0: self.user_model(username="test0"),
            1: self.user_model(username="test1"),
            2: self.user_model(username="test2"),
        }
        for key, user in self.users.items():
            user.save()