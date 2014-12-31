from django.conf.urls import patterns, url, include
from .views import api

itemcomment_patterns = patterns('',
    url(r'^(?P<pk>\d+)/update$',
        api.ItemCommentUpdate.as_view(), name='update'),
)


urlpatterns = patterns('',
    url(r'^comments/',
        include(itemcomment_patterns, namespace="itemcomment")),
)
