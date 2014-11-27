from django.conf.urls import patterns, url, include
from django.contrib import admin
from kii.app import core

kii_urls = core.apps.get_apps_urls()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),    
    url(r'^kii/(?P<username>\w+)/', include(kii_urls, namespace="kii_user")),
    url(r'^kii/', include(kii_urls, namespace="kii")),
)
