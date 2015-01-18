from django.db import models
from django.core.urlresolvers import reverse

from kii import stream

class StreamItemChild1(stream.models.StreamItem):
    def reverse_custom_detail(self, **kwargs):
        
        return reverse("kii:test_stream:streamitemchild1:detail", 
                       kwargs={"pk": self.pk})

class StreamItemChild2(stream.models.StreamItem):
    pass