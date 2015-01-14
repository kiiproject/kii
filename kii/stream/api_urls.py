from django.conf.urls import patterns, url, include
from .views import api

itemcomment_patterns = patterns('',
    url(r'^(?P<pk>\d+)/update$',
        api.ItemCommentUpdate.as_view(), name='update'),
)

stream_patterns = patterns('',
    url(r'^select/(?P<pk>\d+)$',
        api.StreamSelect.as_view(), name='select'),
)
urlpatterns = patterns('',
    url(r'^comments/',
        include(itemcomment_patterns, namespace="itemcomment")),
    url(r'^streams/', include(stream_patterns, namespace="stream")),
)
