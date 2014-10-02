import app
import django




class UserTestCase(app.tests.base.BaseTestCase):

    def setUp(self):
        self.user_model = django.contrib.auth.get_user_model()
        super(UserTestCase, self).setUp()
        
        self.users = {
            0: self.user_model(username="test0"),
        }
        for u in self.user_model.objects.all():
            print(u.username)
        for key, user in self.users.items():
            user.save()