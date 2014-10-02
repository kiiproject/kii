from app import core, registries


class TestApp1(core.App):
    pass

test_app_1 = TestApp1()
registries.app_registry.register(test_app_1, name="test_app_1")


class TestApp2(core.App):
    pass

test_app_2 = TestApp2()
registries.app_registry.register(test_app_2, name="test_app_2")