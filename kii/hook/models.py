from kii import base_models
from django.db import models
from kii.utils import meta
from .core import HookManager

def field_getter(field_name):
    """Returns the actual function for getting a field value (with hooks called on it)"""

    def hooks(self):
        v = getattr(self, field_name)
        for hook in self.hooks.get("get_{0}".format(field_name)):
            v = hook(v)
        return v
    return hooks


class HookMeta(type):
    """Add a get_* method for each field 
    Allow registration of hooks that will be called inside this method, in order to transform
    the output of a field"""

    def __new__(meta, class_name, bases, class_dict):
        
        cls = super(HookMeta, meta).__new__(meta, class_name, bases, class_dict)
        for field in cls._meta.fields:
            setattr(cls, "get_{0}".format(field.name), field_getter(field.name))
        return cls

class HookMixin(base_models.models.BaseMixin):
    hooks = HookManager()
    __metaclass__ = meta.classmaker((HookMeta,))
