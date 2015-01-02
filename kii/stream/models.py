from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from guardian.shortcuts import get_anonymous_user
from polymorphic import (PolymorphicModel, PolymorphicManager,
                         PolymorphicQuerySet)
from actstream import action
from actstream.actions import follow

from kii.base_models import models as base_models_models
from kii.permission import models as permission_models
from kii.discussion import models as discussion_models
from kii.hook.models import HookMixin


class StreamManager(permission_models.PermissionMixinQuerySet.as_manager().__class__): # NOQA
    def get_user_stream(self, user):
        """:return: The main stream of the given user"""
        return self.get(title=user.username, owner=user)


class Stream(permission_models.PermissionMixin, base_models_models.TitleMixin,
             base_models_models.ContentMixin, HookMixin, ):
    """A place were StreamItem instances will be published.

    Think of it as a timeline, a wall, a list of element, such as blog entries
    for exemple, but more generic"""

    objects = StreamManager()

    class Meta(permission_models.PermissionMixin.Meta):
        unique_together = ('owner', 'title')

    def reverse_detail(self, **kwargs):
        return reverse("kii:user_area:stream:index",
                       kwargs={"username": self.owner.username})

    def reverse_update(self, **kwargs):
        """:return: The update URL of the instance"""
        return reverse(self.url_namespace(**kwargs) + "update")

    def reverse_feed(self, **kwargs):
        return reverse("kii:user_area:stream:stream:feed.atom",
                       kwargs={"username": self.owner.username})

    def __str__(self):
        return "<Stream: {0}>".format(self.title)


class StreamItemQuerySet(PolymorphicQuerySet,
                         permission_models.InheritPermissionMixinQuerySet):
    def readable_by(self, target):
        """Exclude draft items for not owners"""
        queryset = super(StreamItemQuerySet, self).readable_by(target)
        return queryset.filter(models.Q(status='pub') | models.Q(owner=target.pk))


class StreamItemQueryManager(
        PolymorphicManager,
        permission_models.InheritPermissionMixinQuerySet.as_manager().__class__): # NOQA

    def get_queryset(self):
        return StreamItemQuerySet(self.model, using=self._db).select_related(
            'owner','root')

    def public(self):
        return self.readable_by(get_anonymous_user())


class StreamItem(PolymorphicModel,
                 base_models_models.TitleMixin,
                 base_models_models.ContentMixin,
                 base_models_models.StatusMixin,
                 base_models_models.TimestampMixin,
                 discussion_models.DiscussionMixin,
                 HookMixin,
                 permission_models.InheritPermissionMixin,):
    """A base class for streamable models"""

    root = models.ForeignKey(Stream, related_name="children")

    objects = StreamItemQueryManager()

    class Meta(PolymorphicModel.Meta,
               permission_models.InheritPermissionMixin.Meta):
        ordering = ['-publication_date']

    def reverse_delete(self, **kwargs):
        return reverse("kii:stream:streamitem:delete",
                       kwargs={"pk": self.pk})

    def reverse_detail(self, **kwargs):
        return reverse("kii:user_area:stream:streamitem:detail",
                       kwargs={"pk": self.pk, "username": self.owner.username})

    def reverse_comment_create(self, **kwargs):
        """Return URL for posting a comment"""
        return reverse("kii:user_area:stream:streamitem:comment_create",
                       kwargs={"username": self.owner.username, "pk": self.pk})


class ItemComment(discussion_models.CommentMixin):

    subject = models.ForeignKey(StreamItem, related_name="comments")


def create_user_stream(sender, instance, created, **kwargs):
    """Create a stream for new users and make the user follow his stream"""
    if created:
        # create a new stream, set title after the owner
        stream = Stream(title=instance.username, owner=instance)
        stream.save()

        # follow the newly crated stream
        follow(instance, stream, actor_only=False)


post_save.connect(create_user_stream, sender=settings.AUTH_USER_MODEL)

def send_new_comment_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user or get_anonymous_user()
        action.send(user, verb='created comment', action_object=instance,
                    target=instance.subject.root)


post_save.connect(send_new_comment_notification, sender=ItemComment)

