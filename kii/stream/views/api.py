from rest_framework import generics
from django.shortcuts import get_object_or_404

from .. import models, serializers, permissions


class ItemCommentUpdate(generics.UpdateAPIView): 

    queryset = models.ItemComment.objects.all().select_related("subject", "user", "user_profile")
    serializer_class = serializers.ItemCommentSerializer

    permission_classes = (permissions.IsCommentModerator,)

