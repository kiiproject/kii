from ..base_models import models as bm
from django.db import models

class Stream(bm.NameMixin):
    pass
    
class StreamItem(bm.NameMixin):

    stream = models.ForeignKey(Stream, related_name="items")