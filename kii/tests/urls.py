from django.conf.urls import patterns, url, include
from django.contrib import admin
from kii import app

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),    
    url(r'^kii/', include(app.core.apps.get_apps_urls(), namespace="kii")),
)
