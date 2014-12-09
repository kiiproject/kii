from django.db import models
from six import with_metaclass

from kii import base_models
from kii.utils import meta
from . import model_filters


class HookMixin(base_models.models.BaseMixin):    

    class Meta:
        abstract = True

    def _filter_field(self, field_name):
        
        return model_filters.filter(field_name, instance=self)

    def __getattribute__(self, name):
        splitted = name.split("_", 1)
        if splitted[0] == "filtered" and splitted[1] in self._meta.get_all_field_names():
            return self._filter_field(splitted[1])
        else:
            # Default behaviour
            return super(HookMixin, self).__getattribute__(name)