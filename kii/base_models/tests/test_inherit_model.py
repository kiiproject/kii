from kii.app.tests import base
from kii.tests import test_base_models
import django
from django_dynamic_fixture import G


class TestNameMixin(base.BaseTestCase):

    
    def test_inherit_model_default_value_to_parent(self):
        p = G(test_base_models.models.NameModel, name="hello")
        i = G(test_base_models.models.InheritNameModel, parent=p)

        self.assertEqual(i.name, "hello")

    def test_inherit_model_can_disable_inheritance(self):
        p = G(test_base_models.models.NameModel, name="hello")
        i = G(test_base_models.models.InheritNameModel, parent=p, inherit_name=False, name="yolo")

        self.assertEqual(i.name, "yolo")

    def test_change_on_parent_model_change_inheriting_model(self):
        p = G(test_base_models.models.NameModel, name="hello")
        i = G(test_base_models.models.InheritNameModel, parent=p)

        self.assertEqual(i.name, "hello")

        p.name = "yolo"
        p.save()

        self.assertEqual(test_base_models.models.InheritNameModel.objects.get(pk=i.pk).name, "yolo")
        
    def test_setting_inheritance_to_true_replace_inherited_value_with_parents(self):
        p = G(test_base_models.models.NameModel, name="hello")
        i = G(test_base_models.models.InheritNameModel, parent=p, inherit_name=False, name="yolo")

        self.assertEqual(i.name, "yolo")

        i.inherit_name = True
        i.save()

        self.assertEqual(test_base_models.models.InheritNameModel.objects.get(pk=i.pk).name, "hello")

    def test_setting_inheritance_to_false_replace_inherited_value_with_given_value(self):
        p = G(test_base_models.models.NameModel, name="hello")
        i = G(test_base_models.models.InheritNameModel, parent=p, inherit_name=True)

        self.assertEqual(i.name, "hello")

        i.inherit_name = False
        i.name = "yolo"
        i.save()

        self.assertEqual(test_base_models.models.InheritNameModel.objects.get(pk=i.pk).name, "yolo")
