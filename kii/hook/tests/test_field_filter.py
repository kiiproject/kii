import kii.app.tests.base
from kii.tests.test_hook import models
from .. import model_filters


class TestFieldFilter(kii.app.tests.base.BaseTestCase):

    def test_can_register_filter(self):
        def uppercase(value, **kwargs):
            return value.capitalize()

        model_filters.register(models.NameModel, "name", uppercase)
        self.assertEqual(model_filters.get(models.NameModel, "name"), [uppercase])

    def test_filtered_field_returns_field_value_if_no_hook(self):
        m = models.NameModel(name="hello")
        self.assertEqual(m.filtered_name, "hello")

    def test_filters_apply(self):

        def uppercase(value, **kwargs):
            return value.capitalize()

        model_filters.register(models.NameModel, "name", uppercase)

        m = models.NameModel(name="hello")
        self.assertEqual(m.filtered_name, "Hello")

    def test_multiple_hooks_are_called_sequentially(self):

        def removefirstletter(value, **kwargs):
            return value[1:]

        def uppercase(value, **kwargs):
            return value.capitalize()

        model_filters.register(models.NameModel, "name", removefirstletter)
        model_filters.register(models.NameModel, "name", uppercase)

        m = models.NameModel(name="hello")
        self.assertEqual(m.filtered_name, "Ello")

    def tearDown(self):
        model_filters.clear()
