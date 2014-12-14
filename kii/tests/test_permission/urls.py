from django.conf.urls import patterns, url, include
from kii.permission import views
from . import models



permissionmodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.PermissionMixinDetail.as_view(
            model=models.PermissionModel, 
            template_name="templates/test.html"), 
        name='detail'),
    url(r'^(?P<pk>\d+)/update', 
        views.PermissionMixinUpdate.as_view(
            model=models.PermissionModel, 
            template_name="templates/test.html"), 
        name='update'),
    url(r'^(?P<pk>\d+)/delete', 
        views.PermissionMixinDelete.as_view(
            model=models.PermissionModel, 
            template_name="templates/test.html"), 
        name='delete'),
    url(r'^$', 
        views.PermissionMixinList.as_view(
            model=models.PermissionModel, 
            template_name="templates/test.html"), 
        name='list'),
)

urlpatterns = patterns('',
    
    url(
        r'^permissionmodel/', 
        include(
            permissionmodel_patterns, 
            namespace='permissionmodel', 
            app_name='permissionmodel')
        ),
)