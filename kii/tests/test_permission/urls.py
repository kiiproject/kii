from django.conf.urls import patterns, url, include
from kii.permission import views
import models



permissionmodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.PermissionMixinDetail.as_view(
            model=models.PermissionModel, 
            template_name="templates/test.html"), 
        name='detail'),
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