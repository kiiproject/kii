from django.conf.urls import patterns, url, include
from kii.base_models import views
import models

namemodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.NameModel), 
        name='detail'),
)

urlpatterns = patterns('',
    url(
        r'^namemodel/', 
        include(
            namemodel_patterns, 
            namespace='namemodel', 
            app_name='namemodel')
        ),
)