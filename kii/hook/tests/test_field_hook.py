import kii.app.tests.base
from kii.tests.test_hook import models

class TestFieldHook(kii.app.tests.base.BaseTestCase):

    def test_fieldhookmixin_has_get_field_method(self):

        model = models.NameModel
        self.assertEqual(hasattr(model, "get_name"), True)

    def test_get_field_returns_field_value_if_no_hook(self):
        m = models.NameModel(name="hello")
        self.assertEqual(m.get_name(), "hello")

    def test_hooks_apply(self):

        def uppercase(value):
            return value.capitalize()

        models.NameModel.hooks.register(uppercase, "get_name")

        m = models.NameModel(name="hello")
        self.assertEqual(m.get_name(), "Hello")

    def test_multiple_hooks_are_called_sequentially(self):

        def removefirstletter(value):
            return value[1:]

        def uppercase(value):
            return value.capitalize()

        models.NameModel.hooks.register(removefirstletter, "get_name")
        models.NameModel.hooks.register(uppercase, "get_name")

        m = models.NameModel(name="hello")
        self.assertEqual(m.get_name(), "Ello")

