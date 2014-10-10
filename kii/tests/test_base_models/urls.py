from django.conf.urls import patterns, url, include
from kii.base_models import views
from . import models

titlemodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.TitleModel), 
        name='detail'),
    url(r'$', 
        views.List.as_view(model=models.TitleModel, template_name="templates/test.html"), 
        name='list'),
)
ownermodel_patterns = patterns('',
    url(r'^create$', 
        views.OwnerMixinCreate.as_view(
            model=models.OwnerModel, 
            template_name="base_models/modelform.html",
            fields=['useless_field']), 
        name='create'),
)

urlpatterns = patterns('',
    url(
        r'^titlemodel/', 
        include(
            titlemodel_patterns, 
            namespace='titlemodel', 
            app_name='titlemodel')
        ),
    url(
        r'^ownermodel/', 
        include(
            ownermodel_patterns, 
            namespace='ownermodel', 
            app_name='ownermodel')
        ),
)