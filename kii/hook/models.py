from kii import base_models
from django.db import models
from kii.utils import meta
from . import model_filters
from six import with_metaclass


def field_getter(field_name):
    """Returns the actual function for getting a field value (with registered filters called on it)"""

    def filter_field(self):
        v = getattr(self, field_name)
        return model_filters.filter(field_name, instance=self)

    return filter_field


class HookMeta(models.base.ModelBase):
    """Add a get_* method for each field 
    Allow registration of hooks that will be called inside this method, in order to transform
    the output of a field"""

    def __new__(meta, class_name, bases, class_dict):
        
        cls = super(HookMeta, meta).__new__(meta, class_name, bases, class_dict)
        for field in cls._meta.fields:
            setattr(cls, "filtered_{0}".format(field.name), property(field_getter(field.name)))
        return cls


class HookMixin(with_metaclass(HookMeta, base_models.models.BaseMixin)):
    pass
