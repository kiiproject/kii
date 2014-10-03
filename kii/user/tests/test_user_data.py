from . import base
from ...tests import test_user

class TestUserData(base.UserTestCase):
    
    def test_user_data_created_when_user_is_saved(self):
        u = self.user_model(username="hello")
        u.save()
        self.assertEqual(u.data.__class__.__name__, "UserData")

    def test_can_link_model_to_user_data(self):
        m = self.users[0].data
        recipe = test_user.models.Recipe(name="Something", userdata=m)
        recipe.save()
        m.recipes.add(recipe)
        