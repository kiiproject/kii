from kii import base_models, user
from django.db import models

class Recipe(base_models.models.TitleMixin):
    userdata = models.ForeignKey(user.models.UserData, related_name="recipes")