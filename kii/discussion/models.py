from __future__ import unicode_literals
from kii import base_models
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings




class AnonymousCommenterProfile(models.Model):

    username = models.CharField(max_length=50)
    email = models.EmailField()
    url = models.URLField()


class CommentMixin(
    base_models.models.ContentMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)ss", editable=False, null=True, blank=True, default=None)
    
    # for anonymous users
    user_profile = models.ForeignKey(AnonymousCommenterProfile, null=True, default=None, blank=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):

        if self.user is None and self.user_profile is None:
            raise IntegrityError(_('Comments require either an authenticated user, either an AnonymousCommenterProfile'))

        return super(CommentMixin, self).save(**kwargs)


class DiscussionMixin(base_models.models.BaseMixin):

    class Meta:
        abstract = True
