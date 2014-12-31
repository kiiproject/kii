from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from kii.base_models import models as bm
from kii.hook import signals


class ProfileWrapper(object):
    """Utility class to access comment user data the same way for anonymous and
    authenticated users."""

    def __init__(self, instance):
        self.instance = instance

    @property
    def url(self):

        if self.instance.user is not None:
            return None
        return self.instance.user_profile.url

    @property
    def username(self):

        if self.instance.user is not None:
            return self.instance.user.username
        return self.instance.user_profile.username

    @property
    def email(self):

        if self.instance.user is not None:
            return self.instance.user.email
        return self.instance.user_profile.email


class AnonymousCommenterProfile(models.Model):
    """Store informations about anonymous user who leave comments."""

    #TODO: ad an ip_adress field
    username = models.CharField(max_length=50)
    email = models.EmailField()
    url = models.URLField()


class CommentQuerySet(bm.BaseMixinQuerySet):
    def public(self):
        """Return public comments (not junk or awaiting moderation)"""
        return self.filter(status="published").select_related("user",
                                                              "user_profile")


class CommentMixin(bm.TimestampMixin, bm.ContentMixin):
    """A base class for comment models.

    Must be linked to either an authenticated user via the :py:attr:`user`
    attribute or an anonymous user via :py:attr:`user_profile`.

    Subclasses MUST implement a ``subject`` ForeignKey field to the model that
    should accept comments.
    """

    #: relationship to an authenticated user
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="%(class)ss", editable=False,
                             null=True, blank=True, default=None)

    #: relationship to an anonymous user
    user_profile = models.ForeignKey(AnonymousCommenterProfile, null=True,
                                     default=None, blank=True)

    profile = None
    """: reference to a :py:class:`ProfileWrapper` instance. Will be set
    automatically on init
    """

    objects = CommentQuerySet.as_manager()

    STATUS_CHOICES = (
        ('published', _('published')),
        ('awaiting_moderation', _('awaiting moderation')),
        ('disapproved', _('disapproved')),
        ('junk', _('junk')),
    )

    status = models.CharField(max_length=255, choices=STATUS_CHOICES,
                              default="awaiting_moderation")

    class Meta:
        abstract = True
        ordering = ['created', ]

    def __init__(self, *args, **kwargs):
        super(CommentMixin, self).__init__(*args, **kwargs)
        # create profile wrapper for easier attribute accesss
        self.profile = ProfileWrapper(self)

    def save(self, **kwargs):
        if self.new:
            if self.user is not None and self.user_profile is not None:
                raise ValidationError(_('You cannot create a comment with'
                                        'both user and user_profile'))

            if self.user is None and self.user_profile is None:
                raise ValidationError(
                    _('Comments require either an authenticated user, either'
                      'an AnonymousCommenterProfile')
                )

            if not self.subject.discussion_open:
                raise ValidationError(
                    _('You cannot register a comment for model instance that'
                      'has discussion_open set to False')
                )

            if not self.content.raw:
                raise ValidationError(_("You cannot post an empty comment"))

            if self.status == "awaiting_moderation":
                results = self.send(comment_detect_junk, instance=self)
                # only set junk to True if all receiver think the comment is junk
                if results:
                    junk = all(junk for receiver, junk in results)
                    if junk:
                        self.status = "junk"

            if self.user is not None:
                self.status = "published"

        # update profile wrapper for easier attribute accesss
        self.profile = ProfileWrapper(self)
        return super(CommentMixin, self).save(**kwargs)

    def is_junk(self):
        return self.status == "junk"

# signals

comment_detect_junk = signals.InstanceSignal()


class DiscussionMixin(bm.BaseMixin):
    """A mixin for models that accept comments"""

    #: whether the model instance is open to discussion or not
    discussion_open = models.BooleanField(default=True)

    class Meta:
        abstract = True
