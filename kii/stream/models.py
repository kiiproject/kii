import base_models
from django.db import models

class Stream(base_models.models.NameMixin):
    pass
    
class StreamItem(base_models.models.NameMixin):

    stream = models.ForeignKey(Stream, related_name="items")