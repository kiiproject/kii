from kii.app import models

class TestModel1(models.AppModel):
    pass

class TestModel2(models.AppModel):
    pass

class TestAppModel(models.AppModel):
    pass

class PublicModel(models.AppModel):
    public = True