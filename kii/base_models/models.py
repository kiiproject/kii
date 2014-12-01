from __future__ import unicode_literals
from django.db import models
import inspect
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils import timezone

from . import fields
from kii.app.models import AppModel
from kii import user

class BaseMixinQuerySet(QuerySet):
    pass


class BaseMixin(AppModel):
    """Add some common behaviour to all mixins"""

    objects = BaseMixinQuerySet.as_manager()

    queryset = BaseMixinQuerySet

    list_item_template = "base_models/basemixin/list_item.html"
    
    class Meta:
        abstract = True

    @classmethod
    def class_name(cls):
        try:
            return cls.__name__.lower()
        except: 
            # instance passed instead of class
            return cls.__class__.__name__.lower()

    def meta(self):
        """For metadata access in template (underscored attributes are forbidden in django templates)"""
        return self._meta

    def save(self, **kwargs):
        # force model validation
        self.clean()
        return super(BaseMixin, self).save(**kwargs)    

    @property
    def new(self):
        """Shortcut to check if instance is already saved or not"""
        return self.pk is None

    def send(self, signal, instance, **kwargs):
        """Send the given signal"""
        return signal.send(sender=instance.__class__, instance=instance)

    @classmethod
    def get_template_names(cls, suffix):
        """Return a list of templates name corresponding to the given suffix (detail, list, etc.). Will include templates 
        from parent classes, if any"""

        def get_template(model, suffix):
            try:
                app_name = model._meta.app_label
                model_name = model.__name__.lower()
                return "{0}/{1}/{2}.html".format(app_name, model_name, suffix)
            except AttributeError:
                return None
        models = (cls,) + inspect.getmro(cls)

        template_names = []
        for model in models:
            t = get_template(model, suffix)
            if t is not None:
                template_names.append(t)

        return template_names
        

class TitleMixin(BaseMixin):

    """An abstract base class for models with a title"""

    title = models.CharField(_('base_models.namemixin.title'), max_length=255, blank=False)

    class Meta:
        abstract = True

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.title == '':
            raise ValidationError('Empty title is not allowed')

        super(TitleMixin, self).clean()


    def __unicode__(self):
        return u'{0}'.format(self.title)


class ContentMixin(BaseMixin):

    content = fields.MarkupField(default_markup_type="markdown")
    class Meta:
        abstract = True


class TimestampMixin(BaseMixin):
    """Add two fields that are automatically set"""
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class StatusMixin(BaseMixin):
    """Add a status and a publication_date field"""
    STATUS_CHOICES = (
        ('dra', _('base_models.status_mixin.draft')),
        ('pub', _('base_models.status_mixin.published')),
    )

    status = models.CharField(choices=STATUS_CHOICES, default="pub", max_length=5)
    publication_date = models.DateTimeField(editable=False, default=None, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Set publication_date to now if status is set to published"""
        if self.publication_date is None and self.status == "pub":
            self.publication_date = timezone.now()

        super(StatusMixin, self).save(*args, **kwargs)


class OwnerMixinQuerySet(BaseMixinQuerySet):
    def owned_by(self, user):
        return self.filter(owner=user.pk)


class OwnerMixin(BaseMixin):
    """A mixin for model instance that have an owner"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(class)ss", editable=False)
    objects = OwnerMixinQuerySet.as_manager()
    

    def owned_by(self, user):
        """return True if instance is owned by given user"""
        return user.pk == self.owner.pk
        
    class Meta:
        abstract = True



class BaseInheritModel(models.Model):
        """Base class for inheriting model (see below)"""

        class Meta:
            abstract = True


def get_inherit_model(local_field, target, target_class, target_related_name, target_field=None):
    """Return a model that will allow field synchronisation between an instance field and a target field
    The returned model will have boolean field `inherit_<local_field>`. 

    .. local_field: the field on subclass that should be synchronized (string)
    .. target: the foreignkey field on subclass from which the value will be retrieved when needed (string)
    .. target_class: the ForeignKey class, for signal activation
    .. target_related_name: the related name on which you can query instances from target, used in post_save signal
    .. target_field: the field name on target from which the value will be retrieved. Default to the same as local_field

    When this field is set to True on a model instance, the value of local_field will be automatically 
    fetched from target.target_field. Inherit from must be a string pointing
    to a ForeignKey field on instance, with a field named target_field, 
    from which the value will be inherited

    This method will also return a dict of signals you have to register manually in order to enable field synchronization

    Warning: field synchronization won't work if you use the returned model in a abstract base class
    """
    target_field = target_field or local_field
    inherit_model_config = (local_field, target, target_field)        


    InheritModel = type(
        str('InheritModel_{0}_{1}_{2}'.format(local_field, target, target_field)), 
        (BaseInheritModel,), 
        {
            str('inherit_{0}'.format(local_field)): models.BooleanField(default=True),
            str('_inherit_config_{0}'.format(local_field)): inherit_model_config,
            str('Meta'): BaseInheritModel.Meta,
            str('__module__'): __name__
        })

    def inheriting_pre_save_signal(sender, instance, **kwargs):
        if not issubclass(sender, InheritModel) or not hasattr(instance, target):
            return

        # set local_field value to target field value if needed
        if getattr(instance, "inherit_{0}".format(local_field)) is True:
            t = getattr(instance, target)
            t_value = getattr(t, target_field)
            setattr(instance, local_field, t_value)

    def target_post_save_signal(sender, instance, **kwargs):

        if not issubclass(sender, target_class):
            return

        filters = {"inherit_{0}".format(local_field): True}
        instances = getattr(instance, target_related_name).filter(**filters)

        # update inheriting instance when target value change
        for i in instances:
            i.save()

    signals = {"pre_save": inheriting_pre_save_signal, 'post_save':target_post_save_signal}
    
    return InheritModel, signals
    
