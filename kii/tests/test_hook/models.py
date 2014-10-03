from kii import hook
from django.db import models

class NameModel(hook.models.HookMixin):
    name = models.CharField(max_length=150)

