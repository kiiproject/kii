from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from kii import user
from django.conf import settings
from django.core.urlresolvers import reverse


class BaseMixin(models.Model):
    """Add some common behaviour to all mixins"""

    class Meta:
        abstract = True

    def save(self, **kwargs):
        # force model validation
        self.clean()
        return super(BaseMixin, self).save(**kwargs)

    @property
    def url_namespace(self):
        """Return the URL namespace of the class, such as `app_label:model_label:`"""
        app_name = self._meta.app_label
        model_name = self.__class__.__name__.lower()

        return "{0}:{1}:".format(app_name, model_name)

    def reverse(self, suffix):
        """Return a reversed URL for given suffix (for example: detail, list, edit...)
        you can override per-suffix URLs by defining .reverse_<suffix> methods
        """

        if hasattr(self, 'reverse_{0}'.format(suffix)):
            return getattr(self, 'reverse_{0}'.format(suffix))()  
                      
        return reverse(self.url_namespace + suffix)
        
    def reverse_detail(self):
        return reverse(self.url_namespace + "detail", kwargs={"pk":self.pk})

    def get_absolute_url(self):
        return self.reverse_detail()


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

    def owned_by(self, user):
        """return True if instance is owned by given user"""
        return user.pk == self.owner.pk
        
    class Meta:
        abstract = True


