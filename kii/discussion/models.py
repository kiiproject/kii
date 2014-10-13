from __future__ import unicode_literals
from kii import base_models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey




class CommentMixin(base_models.models.BaseMixin):

    pass


class DiscussionMixin(base_models.models.BaseMixin):

    class Meta:
        abstract = True
