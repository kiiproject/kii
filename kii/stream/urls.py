from django.conf.urls import patterns, url, include
from . import views

streamitem_patterns = patterns('',
    url(r'^(?P<pk>\d+)$', views.Detail.as_view(), name='detail'), # NOQA
    url(r'^(?P<pk>\d+)/delete$', views.Delete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/comments/add$', views.ItemCommentCreate.as_view(),
        name='comment_create'),
)

itemcomment_patterns = patterns('',
    url(r'^$', views.ItemCommentList.as_view(), name='list'), # NOQA
    url(r'^moderation$', views.ItemCommentModeration.as_view(),
        name='moderation'),
)

stream_patterns = patterns('',
    url(r'^$', views.List.as_view(), name='index'), # NOQA
    url(r'^update$', views.StreamUpdate.as_view(), name='update'), # NOQA
    url(r'^feed/atom$', views.StreamFeedAtom(), name='feed.atom'),
    url(r'^items/', include(streamitem_patterns, namespace="streamitem")),
    url(r'^comments/', include(itemcomment_patterns, namespace="itemcomment")),
)

urlpatterns = patterns('',
    url(r'^stream/(?P<stream>\w+)/', include(stream_patterns, namespace="stream")),
    url(r'^items/', include(streamitem_patterns, namespace="streamitem")),
)
