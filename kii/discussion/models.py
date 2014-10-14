from __future__ import unicode_literals

from kii import base_models
from kii.hook import signals

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings





class ProfileWrapper(object):
    """Utility class to return either user or user_profile attributes on comments"""

    def __init__(self, instance):
        self.instance = instance

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

    username = models.CharField(max_length=50)
    email = models.EmailField()
    url = models.URLField()


class CommentMixin(
    base_models.models.ContentMixin):

    """Subclass MUST implement a subject ForeignKey field to the model that is commented"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)ss", editable=False, null=True, blank=True, default=None)
    
    # for anonymous users
    user_profile = models.ForeignKey(AnonymousCommenterProfile, null=True, default=None, blank=True)

    published = models.BooleanField(default=False)

    # Set this to true for spam comments
    unwanted = models.BooleanField(default=False)

    profile = None

    # signals

    

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):

        super(CommentMixin, self).__init__(*args, **kwargs)
        # create profile wrapper for easier attribute accesss
        self.profile = ProfileWrapper(self)

    def save(self, **kwargs):


        if self.user is not None and self.user_profile is not None:
            raise IntegrityError(_('You cannot create a comment with both user and user_profile'))
            
        if self.user is None and self.user_profile is None:
            raise IntegrityError(_('Comments require either an authenticated user, either an AnonymousCommenterProfile'))

        if not self.subject.discussion_open:
            raise ValueError(_("You cannot register a comment for model instance that has discussion_open set to False"))
        
        if self.new:
            results = self.send(comment_detect_unwanted, instance=self)
            
            # only set unwanted to True if all receiver think the comment is unwanted
            self.unwanted = all(unwanted for receiver, unwanted in results)

        if self.unwanted:
            self.published = False

        elif self.user is not None:
            self.published = True

        # update profile wrapper for easier attribute accesss
        self.profile = ProfileWrapper(self)

        return super(CommentMixin, self).save(**kwargs)


# signals

comment_detect_unwanted = signals.InstanceSignal()

class DiscussionMixin(base_models.models.BaseMixin):

    discussion_open = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
