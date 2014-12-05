from django.core.urlresolvers import reverse_lazy
from django.http import Http404

from . import models
from kii.base_models import views

class Index(views.RequireAuthenticationMixin, views.OwnerMixinDetail):

    template_name = "stream/stream/detail.html"
    streamitem_class = None
    def get_object(self):

        try:
            return models.Stream.objects.get(owner=self.request.user.pk, title=self.request.user.username)
        except models.Stream.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        items = self.object.children.readable_by(self.request.user)
        if self.streamitem_class is not None:
            # filter items using given class
            items = items.select_subclasses(self.streamitem_class)
        context["items"] = items
        return context
        

class Create(views.OwnerMixinCreate):
    success_url = reverse_lazy('kii:stream:index')


class Update(views.OwnerMixinUpdate):
    success_url = reverse_lazy('kii:stream:index')


class Detail(views.Detail):
    pass


class Delete(views.OwnerMixinDelete):
    model = models.StreamItem

    def get_success_url(self):
        return reverse_lazy("kii:stream:index")

class List(views.OwnerMixinList):
    pass