from django.conf.urls import patterns, url, include
from kii.stream.views import Detail

from .models import StreamItemChild1

streamitemchild1_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        Detail.as_view(model=StreamItemChild1), 
        name='detail'),
)


urlpatterns = patterns('',
    url(
        r'^streamitemchild1/', 
        include(
            streamitemchild1_patterns, 
            namespace='streamitemchild1', 
            app_name='streamitemchild1')
        ),
)