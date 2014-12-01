from django.conf.urls import patterns, url, include
from . import views

streamitem_patterns = patterns('',
    url(r'^(?P<pk>\d+)/delete$', views.Delete.as_view(), name='delete'),
)



urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^items', include(streamitem_patterns, namespace="streamitem")),
)
