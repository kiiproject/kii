from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.contrib import messages

from . import models, forms
from kii.base_models import views
from kii.permission import views as permission_views
from kii.discussion import views as discussion_views


class StreamContextMixin(object):
    """pass current requested stream into context"""

    current_stream = None
    def get_current_stream(self):
        try:
            self.current_stream = models.Stream.objects.get(owner=self.owner.pk, title=self.owner.username)
            return self.current_stream
        except models.Stream.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(StreamContextMixin, self).get_context_data(**kwargs)
        context['current_stream'] = self.current_stream

        return context

class Index(StreamContextMixin, permission_views.PermissionMixinDetail):

    template_name = "stream/stream/detail.html"
    streamitem_class = None

    def get_object(self):
        return self.get_current_stream()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        items = self.current_stream.children.readable_by(self.request.user).select_related()
        if self.streamitem_class is not None:
            # filter items using given class
            items = items.instance_of(self.streamitem_class)
        context["items"] = items
        return context
        

class Create(views.OwnerMixinCreate):
    success_url = reverse_lazy('kii:stream:index')


class Update(permission_views.PermissionMixinUpdate):
    success_url = reverse_lazy('kii:stream:index')


class Detail(discussion_views.CommentFormMixin, permission_views.PermissionMixinDetail):
    comment_form_class = forms.ItemCommentForm
    model = models.StreamItem


class Delete(permission_views.PermissionMixinDelete):
    model = models.StreamItem

    def get_success_url(self):
        return reverse_lazy("kii:stream:index")

class List(permission_views.PermissionMixinList):
    pass

class StreamUpdate(StreamContextMixin, permission_views.PermissionMixinUpdate):
    model = models.Stream
    form_class = forms.StreamForm

    def get_object(self):

        return self.get_current_stream()

from django.utils.feedgenerator import Atom1Feed

class StreamFeedAtom(StreamContextMixin, views.OwnerMixin, Feed):

    feed_type = Atom1Feed
    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.owner = self.get_owner(request, **kwargs)
        self.stream = self.get_current_stream()

        return super(StreamFeedAtom, self).__call__(request, *args, **kwargs)

    def author_name(self):
        return self.stream.owner.get_full_name()

    def title(self):
        return self.stream.title

    def link(self):
        return self.stream.reverse('detail')

    def items(self):
        return self.stream.children.public()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.filtered_content

    def item_pubdate(self, item):
        return item.publication_date

    def item_updateddate(self, item):
        return item.last_modified

class ItemCommentCreate(discussion_views.CommentCreate):
    form_class = forms.ItemCommentForm