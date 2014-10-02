from ... import app
#from .. import models as um
import models
import django
user_model = django.contrib.auth.get_user_model()

class UserTestCase(app.tests.base.BaseTestCase):

    def setUp(self):

        super(UserTestCase, self).setUp()
        
        self.users = {
            0: user_model(username="test0"),
        }
        for u in user_model.objects.all():
            print(u.username)
        for key, user in self.users.items():
            user.save()

class TestUserData(UserTestCase):
    
    def test_user_data_created_when_user_is_saved(self):
        u = user_model(username="hello")
        u.save()
        self.assertEqual(u.data.__class__.__name__, "UserData")

    def test_can_link_model_to_user_data(self):
        m = self.users[0].data
        recipe = models.Recipe(name="Something")
        recipe.save()
        m.recipes.add(recipe)
        m.save()
        