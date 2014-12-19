from kii.base_models import filterset

from . import models

class StatusFilterSet(filterset.BaseFilterSet):
    class Meta:
        model = models.StatusModel
        fields = {
            'status': ['exact'],
        }