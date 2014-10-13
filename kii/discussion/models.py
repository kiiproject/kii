from __future__ import unicode_literals
from kii import base_models
from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings



class CommentMixin(
    base_models.models.ContentMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)ss", editable=False, null=True, default=None)
    username = models.CharField(max_length=50, default=None, null=True)
    email = models.EmailField(default=False, null=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):

        if self.user is None and (self.username is None or self.email is None):
            raise IntegrityError(_('Username and email are required for anonymous comments'))

        return super(CommentMixin, self).save(**kwargs)



class DiscussionMixin(base_models.models.BaseMixin):

    class Meta:
        abstract = True
