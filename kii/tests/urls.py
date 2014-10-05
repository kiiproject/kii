from django.conf.urls import patterns, url, include
from django.contrib import admin
from kii import app

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(
        r'^test_base_models/', 
        include(
            'kii.tests.test_base_models.urls', 
            namespace='test_base_models', 
            app_name='test_base_models')
        ),
    url(
        r'^test_permission/', 
        include(
            'kii.tests.test_permission.urls', 
            namespace='test_permission', 
            app_name='test_permission')
        ),
    url(r'^kii/', include(app.core.apps.get_apps_urls(), namespace="kii")),
)
