from __future__ import unicode_literals
from .. import base_models, permissions
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class Stream(
    permissions.models.PermissionMixin,
    base_models.models.NameMixin, 
    base_models.models.OwnerMixin):
    """
    A place were StreamItem instances will be published.

    Think of it as a timeline, a wall, a list of element, such as blog entries for exemple,
    but more generic"""

    # The default name for newly created streams
    default_name = _("stream.default_name")

    
class StreamItem(base_models.models.NameMixin):
    """A base class for streamable models"""

    stream = models.ForeignKey(Stream, related_name="items")


def create_user_stream(sender, instance, created, **kwargs):
    if created:
        stream = Stream(name=Stream.default_name, owner=instance)
        stream.save()

post_save.connect(create_user_stream, sender=settings.AUTH_USER_MODEL)