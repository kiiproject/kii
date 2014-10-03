from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from kii import user
from django.conf import settings

class BaseMixin(models.Model):
    """Add some common behaviour to all mixins"""

    def save(self, **kwargs):
        # force model validation
        self.clean()
        return super(BaseMixin, self).save(**kwargs)

    class Meta:
        abstract = True


class NameMixin(BaseMixin):

    """An abstract base class for models with a name"""

    name = models.CharField(_('base_models.namemixin.name'), max_length=255, blank=False)

    class Meta:
        abstract = True

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.name == '':
            raise ValidationError('Empty name is not allowed')

        super(NameMixin, self).clean()


class OwnerMixin(BaseMixin):
    """A mixin for model instance that have an owner"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)ss")

    class Meta:
        abstract = True


