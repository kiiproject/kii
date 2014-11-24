from django.views.generic import DetailView
from django.http import Http404

from . import models


class Index(DetailView):

    template_name = "stream/stream/detail.html"

    def get_object(self):

        try:
            return models.Stream.objects.get(owner=self.request.user.pk, title=self.request.user.username)
        except models.Stream.DoesNotExist:
            raise Http404