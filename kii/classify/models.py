from __future__ import unicode_literals
from kii import base_models, stream as stream_app, permission
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Tag(
    MPTTModel,
    base_models.models.OwnerMixin,
    base_models.models.TitleMixin):
    """
    A model for storing StreamItem instances"""

    streamitems = models.ManyToManyField(stream_app.models.StreamItem, through='TagStreamItem', related_name="tags")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']
        
class TagStreamItem(models.Model):
    """Many to many relationship between StreamItem and Tag"""
    streamitem = models.ForeignKey(stream_app.models.StreamItem)
    tag = models.ForeignKey(Tag)
