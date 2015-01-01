from kii.base_models import filterset

from . import models


class CommentFilterSet(filterset.BaseFilterSet):

    class Meta:
        model = models.ItemComment
        fields = ['status']


class OwnerStreamItemFilterSet(filterset.BaseFilterSet):
    """A filterset that is display only to the owner of a stream"""
    class Meta:
        model = models.StreamItem
        fields = ['status']
