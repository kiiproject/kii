import apps

@apps.test_app_1.models.register
class TestModel1:
    pass

@apps.test_app_1.models.register
class TestModel2:
    pass