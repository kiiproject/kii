from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _

from kii.base_models import views
from kii.permission import views as permission_views
from kii.discussion import views as discussion_views
from .. import models, forms, filterset


class StreamContextMixin(views.OwnerMixin):
    """pass current requested stream into context"""

    current_stream = None

    def get_current_stream(self):
        if self.current_stream is None:
            try:
                self.current_stream = models.Stream.objects.get_user_stream(self.request.owner)
            except models.Stream.DoesNotExist:
                raise Http404

        return self.current_stream

    def get_context_data(self, **kwargs):
        context = super(StreamContextMixin, self).get_context_data(**kwargs)
        context['current_stream'] = self.get_current_stream()

        return context


class List(StreamContextMixin, permission_views.PermissionMixinList):
    
    model = models.StreamItem
    streamitem_class = None
    
    def get_queryset(self, **kwargs):
        queryset = super(List, self).get_queryset(**kwargs)
        if self.streamitem_class:
            queryset = queryset.instance_of(self.streamitem_class)

        return queryset

    def get_filterset_kwargs(self):
        kwargs = super(List, self).get_filterset_kwargs()

        if kwargs['data'].get('status') is None:
            kwargs['data']['status'] = "pub"
        return kwargs

    def get_filterset_class(self):
        if self.get_current_stream().owned_by(self.request.user):
            return filterset.OwnerStreamItemFilterSet


class Create(StreamContextMixin, views.OwnerMixinCreate):
    success_url = reverse_lazy('kii:stream:index')


class Update(StreamContextMixin, permission_views.PermissionMixinUpdate):
    success_url = reverse_lazy('kii:stream:index')


class Detail(StreamContextMixin, discussion_views.CommentFormMixin,
             permission_views.PermissionMixinDetail):
    comment_form_class = forms.ItemCommentForm
    model = models.StreamItem


class Delete(StreamContextMixin, permission_views.PermissionMixinDelete):
    model = models.StreamItem

    def get_success_url(self):
        return reverse_lazy("kii:stream:index")


class StreamUpdate(StreamContextMixin, permission_views.PermissionMixinUpdate):
    model = models.Stream
    form_class = forms.StreamForm

    def get_object(self):

        return self.get_current_stream()

from django.utils.feedgenerator import Atom1Feed


class StreamFeedAtom(StreamContextMixin, views.OwnerMixin, Feed):

    feed_type = Atom1Feed

    def __call__(self, request, *args, **kwargs):
        self.setup(request, *args, **kwargs)
        self.pre_dispatch(request, *args, **kwargs)
        self.owner = request.owner
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


class ItemCommentList(StreamContextMixin, views.MultipleObjectPermissionMixin,
                      views.List):
    required_permission = None
    model = models.ItemComment
    page_title = _("comment.list")

    def get_queryset(self, **kwargs):
        queryset = super(ItemCommentList, self).get_queryset()
        stream = self.get_current_stream()
        return queryset.filter(subject__root=stream).public()


class ItemCommentModeration(StreamContextMixin,
                            views.MultipleObjectPermissionMixin, views.List):

    model = models.ItemComment
    required_permission = True
    template_name = "stream/itemcomment/moderation.html"
    page_title = _("comment.moderation")
    filterset_class = filterset.CommentFilterSet

    def get_filterset_kwargs(self):
        kwargs = super(ItemCommentModeration, self).get_filterset_kwargs()

        if kwargs['data'].get('status') is None:
            kwargs['data']['status'] = "awaiting_moderation"
        return kwargs

    def has_required_permission(self, request, *args, **kwargs):
        stream = self.get_current_stream()

        return stream.owner.pk == request.user.pk

    def get_queryset(self, **kwargs):
        queryset = super(ItemCommentModeration, self).get_queryset()
        stream = self.get_current_stream()
        return queryset.filter(subject__root=stream) \
                       .select_related("subject", "user", "user_profile") \
                       .order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(ItemCommentModeration, self).get_context_data(**kwargs)

        context['can_moderate'] = True
        return context
