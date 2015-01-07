from rest_framework import serializers

from . import models


class ItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemComment
        fields = ('id', 'content', 'status', 'subject')
