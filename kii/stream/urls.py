from django.conf.urls import patterns, url, include
from . import views

streamitem_patterns = patterns('',
    url(r'^(?P<pk>\d+)/delete$', views.Delete.as_view(), name='delete'),
)
stream_patterns = patterns('',
    url(r'^update$', views.StreamUpdate.as_view(), name='update'),
    url(r'^feeds/atom$', views.StreamFeedAtom.as_view(), name='feed.atom'),
)


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^stream/', include(stream_patterns, namespace="stream")),
    url(r'^items/', include(streamitem_patterns, namespace="streamitem")),
)
