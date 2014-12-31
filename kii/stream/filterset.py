from kii.base_models import filterset

from . import models


class CommentFilterSet(filterset.BaseFilterSet):

    class Meta:
        model = models.ItemComment
        fields = ['status']
