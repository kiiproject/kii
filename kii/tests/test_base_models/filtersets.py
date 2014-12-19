import django_filters

from . import models

class StatusFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.StatusModel
        fields = {
            'status': ['exact'],
        }