import base_models, permissions
from django.db import models

class Stream(
    permissions.models.PermissionMixin,
    base_models.models.NameMixin, 
    base_models.models.OwnerMixin):

    pass
    
class StreamItem(base_models.models.NameMixin):

    stream = models.ForeignKey(Stream, related_name="items")