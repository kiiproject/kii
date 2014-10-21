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
titlemodel2_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.TitleModel2), 
        name='detail'),
    url(r'^create$', 
        views.Create.as_view(model=models.TitleModel2), 
        name='create'),
    url(r'^$', 
        views.List.as_view(model=models.TitleModel2), 
        name='list'),
    url(r'^(?P<pk>\d+)/delete$', 
        views.Delete.as_view(model=models.TitleModel2), 
        name='delete'),
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
        r'^titlemodel2/', 
        include(
            titlemodel2_patterns, 
            namespace='titlemodel2', 
            app_name='titlemodel2')
        ),
    url(
        r'^ownermodel/', 
        include(
            ownermodel_patterns, 
            namespace='ownermodel', 
            app_name='ownermodel')
        ),
)