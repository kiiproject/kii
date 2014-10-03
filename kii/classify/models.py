from __future__ import unicode_literals
from kii import base_models, stream as stream_app
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
import django.core.exceptions
from mptt.models import MPTTModel, TreeForeignKey

class Workspace(
    MPTTModel,
    base_models.models.NameMixin):
    """
    A model for storing StreamItem instances"""

    stream = models.ForeignKey(stream_app.models.Stream, related_name="workspaces")
    items = models.ManyToManyField(stream_app.models.StreamItem, through='WorkspaceStreamItem')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        
class WorkspaceStreamItem(models.Model):
    """Many to many relationship between StreamItem and Workspace"""
    item = models.ForeignKey(stream_app.models.StreamItem)
    workspace = models.ForeignKey(Workspace)



def workspace_storableitem_created(sender, instance, **kwargs):
    
    if instance.pk is None:
        # the instance is going to be created
        if instance.workspace.stream is not instance.item.stream:
            raise django.core.exceptions.ValidationError(
                "You cannot store a StreamItem in a Workspace of a different Stream")

pre_save.connect(workspace_storableitem_created, sender=WorkspaceStreamItem)