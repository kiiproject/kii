from user.tests import base
from tests import test_base_models
import django


class TestOwnerMixin(base.UserTestCase):
    
    def test_owner_field(self):
        m = test_base_models.models.OwnerModel(owner=self.users[0])
        m.save()
        
    def test_owner_is_required(self):
        m = test_base_models.models.OwnerModel()
        with self.assertRaises(django.db.IntegrityError):
            m.save()

    def test_can_retrieve_owned_item_via_user(self):
        m = test_base_models.models.OwnerModel(owner=self.users[0])
        m.save()
        self.assertEqual(m, self.users[0].ownermodels.first())