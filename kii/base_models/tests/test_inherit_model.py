from kii.app.tests import base
from kii.tests import test_base_models
import django


class TestInheritModel(base.BaseTestCase):

    
    def test_inherit_model_default_value_to_parent(self):
        p = self.G(test_base_models.models.TitleModel, title="hello")
        i = self.G(test_base_models.models.InheritTitleModel, parent=p)

        self.assertEqual(i.title, "hello")

    def test_inherit_model_can_disable_inheritance(self):
        p = self.G(test_base_models.models.TitleModel, title="hello")
        i = self.G(test_base_models.models.InheritTitleModel, parent=p, inherit_title=False, title="yolo")

        self.assertEqual(i.title, "yolo")

    def test_change_on_parent_model_change_inheriting_model(self):
        p = self.G(test_base_models.models.TitleModel, title="hello")
        i = self.G(test_base_models.models.InheritTitleModel, parent=p)

        self.assertEqual(i.title, "hello")

        p.title = "yolo"
        p.save()

        self.assertEqual(test_base_models.models.InheritTitleModel.objects.get(pk=i.pk).title, "yolo")
        
    def test_setting_inheritance_to_true_replace_inherited_value_with_parents(self):
        p = self.G(test_base_models.models.TitleModel, title="hello")
        i = self.G(test_base_models.models.InheritTitleModel, parent=p, inherit_title=False, title="yolo")

        self.assertEqual(i.title, "yolo")

        i.inherit_title = True
        i.save()

        self.assertEqual(test_base_models.models.InheritTitleModel.objects.get(pk=i.pk).title, "hello")

    def test_setting_inheritance_to_false_replace_inherited_value_with_given_value(self):
        p = self.G(test_base_models.models.TitleModel, title="hello")
        i = self.G(test_base_models.models.InheritTitleModel, parent=p, inherit_title=True)

        self.assertEqual(i.title, "hello")

        i.inherit_title = False
        i.title = "yolo"
        i.save()

        self.assertEqual(test_base_models.models.InheritTitleModel.objects.get(pk=i.pk).title, "yolo")
