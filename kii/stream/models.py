from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from polymorphic import PolymorphicModel, PolymorphicManager, PolymorphicQuerySet
from guardian.shortcuts import get_anonymous_user
import inspect

from kii.base_models import models as base_models_models
from kii.permission import models as permission_models
from kii.discussion import models as discussion_models
from kii.hook.models import HookMixin


class Stream(
    permission_models.PermissionMixin,
    base_models_models.TitleMixin,    
    base_models_models.ContentMixin,):
    """
    A place were StreamItem instances will be published.

    Think of it as a timeline, a wall, a list of element, such as blog entries for exemple,
    but more generic"""

    class Meta(permission_models.PermissionMixin.Meta):
        unique_together = ('owner', 'title')

    def reverse_detail(self, **kwargs):
        return reverse("kii:user_area:stream:index", kwargs={"username": self.owner.username})

    def reverse_feed(self, **kwargs):
        return reverse("kii:user_area:stream:stream:feed.atom", kwargs={"username": self.owner.username})

class StreamItemQuerySet(PolymorphicQuerySet, permission_models.InheritPermissionMixinQueryset):
    def readable_by(self, target):
        """Exclude draft items"""        

        return super(StreamItemQuerySet, self).readable_by(target).filter(status="pub")

    def public(self):
        return self.readable_by(get_anonymous_user())

class StreamItemQueryManager(PolymorphicManager, 
    permission_models.InheritPermissionMixinQueryset.as_manager().__class__):

    def get_queryset(self):
        return StreamItemQuerySet(self.model, using=self._db)

class StreamItem(
    PolymorphicModel,    
    HookMixin, 
    base_models_models.TitleMixin,
    base_models_models.ContentMixin,
    base_models_models.StatusMixin,
    base_models_models.TimestampMixin,
    discussion_models.DiscussionMixin,
    permission_models.InheritPermissionMixin,):

    """A base class for streamable models"""

    root = models.ForeignKey(Stream, related_name="children")

    objects = StreamItemQueryManager()

    class Meta(PolymorphicModel.Meta, permission_models.InheritPermissionMixin.Meta):
        ordering = ['-publication_date']

    def reverse_delete(self, **kwargs):
        return reverse("kii:stream:streamitem:delete", kwargs={"pk":self.pk})

    def reverse_detail(self, **kwargs):
        return reverse("kii:user_area:stream:streamitem:detail", kwargs={"pk":self.pk, "username": self.owner.username})

class StreamItemComment(discussion_models.CommentMixin):

    subject = models.ForeignKey(StreamItem, related_name="comments")

def create_user_stream(sender, instance, created, **kwargs):
    if created:
        # create a new stream, set title after the owner
        stream = Stream(title=instance.username, owner=instance)
        stream.save()

post_save.connect(create_user_stream, sender=settings.AUTH_USER_MODEL)