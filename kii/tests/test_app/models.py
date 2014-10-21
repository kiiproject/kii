from . import apps
from django.db import models


class TestModel1(models.Model):
    
    class Meta:
        verbose_name = "Test Model"

class TestModel2(models.Model):
    pass