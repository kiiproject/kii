from django.conf.urls import patterns, url, include
from kii.base_models import views
import models

namemodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.NameModel), 
        name='detail'),
    url(r'$', 
        views.List.as_view(model=models.NameModel, template_name="templates/test.html"), 
        name='list'),
)
ownermodel_patterns = patterns('',
    url(r'^create$', 
        views.OwnerMixinCreate.as_view(model=models.OwnerModel, template_name="templates/test.html"), 
        name='create'),
)

urlpatterns = patterns('',
    url(
        r'^namemodel/', 
        include(
            namemodel_patterns, 
            namespace='namemodel', 
            app_name='namemodel')
        ),
    url(
        r'^ownermodel/', 
        include(
            ownermodel_patterns, 
            namespace='ownermodel', 
            app_name='ownermodel')
        ),
)