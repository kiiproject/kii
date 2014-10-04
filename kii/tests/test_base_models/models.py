from kii import base_models
from django.db import models


class NameModel(base_models.models.NameMixin):
    pass

class OwnerModel(base_models.models.OwnerMixin):
    useless_field = models.CharField(max_length=255, default="", blank=True)