from __future__ import unicode_literals
from kii import base_models, stream as stream_app, permission
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
import django.core.exceptions
from mptt.models import MPTTModel, TreeForeignKey

class Tag(
    MPTTModel,
    base_models.models.NameMixin):
    """
    A model for storing StreamItem instances"""

    stream = models.ForeignKey(stream_app.models.Stream, related_name="tags")
    items = models.ManyToManyField(stream_app.models.StreamItem, through='TagItem')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        
class TagItem(models.Model):
    """Many to many relationship between StreamItem and Tag"""
    item = models.ForeignKey(stream_app.models.StreamItem)
    tag = models.ForeignKey(Tag)



def tag_storableitem_created(sender, instance, **kwargs):
    
    if instance.pk is None:
        # the instance is going to be created
        if instance.tag.stream is not instance.item.stream:
            raise django.core.exceptions.ValidationError(
                "You cannot store a StreamItem in a Tag of a different Stream")

pre_save.connect(tag_storableitem_created, sender=TagItem)


def set_tag_owner(sender, instance, **kwargs):
    instance.owner = instance.stream.owner

pre_save.connect(set_tag_owner, sender=Tag)