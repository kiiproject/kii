import django_filters

from . import models

class BaseFilterSet(django_filters.FilterSet):
    class Meta:
        pass