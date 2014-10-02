from ... import user
import models
import django


class TestOwnerMixin(user.tests.base.UserTestCase):

    
    def test_owner_field(self):
        m = models.OwnerModel(owner=self.users[0])
        m.save()
        
    def test_owner_is_required(self):
        m = models.OwnerModel()
        with self.assertRaises(django.core.exceptions.ValidationError):
            m.save()