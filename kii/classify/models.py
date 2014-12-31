from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from kii.base_models import models as bm
from kii.stream import models as stream_models


class Tag(
    MPTTModel,
    bm.OwnerMixin,
    bm.TitleMixin):
    """
    Hierarchical model that can be attached to a :py:class:`kii.stream.models.StreamItem` instance.
    """

    streamitems = models.ManyToManyField(stream_models.StreamItem, through='TagStreamItem', related_name="tags")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']
        
        
class TagStreamItem(models.Model):
    """Many to many relationship between StreamItem and Tag"""

    streamitem = models.ForeignKey(stream_models.StreamItem)
    tag = models.ForeignKey(Tag)
