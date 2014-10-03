from django.conf.urls import patterns, url, include
from kii.permission import views
import models

privateread_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.PrivateReadDetail.as_view(
            model=models.PrivateReadModel, 
            template_name="templates/test.html"), 
        name='detail'),
    url(r'^$', 
        views.PrivateReadList.as_view(
            model=models.PrivateReadModel, 
            template_name="templates/test.html"), 
        name='list'),
)

urlpatterns = patterns('',
    url(
        r'^privatereadmodel/', 
        include(
            privateread_patterns, 
            namespace='privatereadmodel', 
            app_name='privatereadmodel')
        ),
)