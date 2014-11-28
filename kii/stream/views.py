from django.views.generic import DetailView
from django.http import Http404

from . import models
from kii.base_models import views

class Index(views.RequireAuthenticationMixin, DetailView):

    template_name = "stream/stream/detail.html"

    def get_object(self):

        try:
            return models.Stream.objects.get(owner=self.request.user.pk, title=self.request.user.username)
        except models.Stream.DoesNotExist:
            raise Http404

class Create(views.RequireAuthenticationMixin, views.Create):
    pass

class Detail(views.Detail):
    pass

class Delete(views.RequireAuthenticationMixin, views.Delete):
    pass

class List(views.Create):
    pass