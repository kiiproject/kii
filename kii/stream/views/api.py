from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions as rest_permissions
from rest_framework.response import Response

from .. import models, serializers, permissions

class ItemCommentUpdate(generics.UpdateAPIView):

    queryset = models.ItemComment.objects.all()\
                                         .select_related("subject", "user",
                                                         "user_profile")
    serializer_class = serializers.ItemCommentSerializer

    permission_classes = (permissions.IsCommentModerator,)


class StreamSelect(views.APIView):
    """Save the given stream as default in user's session"""

    permissions = (rest_permissions.IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        
        try:
            stream = models.Stream.objects.get(owner=request.user, pk=kwargs.get('pk'))
            request.session['selected_stream'] = stream.pk
            return Response('', status=status.HTTP_200_OK)
        except models.Stream.DoesNotExist:
            return Response('', status=status.HTTP_404_NOT_FOUND)
