import base_models, user
from django.conf import settings
from django.db import models

class Recipe(base_models.models.NameMixin):
    userdata = models.ForeignKey(user.models.UserData, related_name="recipes")