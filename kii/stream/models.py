from __future__ import unicode_literals
from .. import base_models, permission
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class Stream(
    permission.models.PermissionMixin,
    base_models.models.TitleMixin):
    """
    A place were StreamItem instances will be published.

    Think of it as a timeline, a wall, a list of element, such as blog entries for exemple,
    but more generic"""

    pass

    
class StreamItem(
    base_models.models.TitleMixin,
    base_models.models.StatusMixin):
    """A base class for streamable models"""

    stream = models.ForeignKey(Stream, related_name="items")


def create_user_stream(sender, instance, created, **kwargs):
    if created:
        # create a new stream, set title after the owner
        stream = Stream(title=instance.username, owner=instance)
        stream.save()

post_save.connect(create_user_stream, sender=settings.AUTH_USER_MODEL)