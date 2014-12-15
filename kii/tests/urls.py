from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin
from kii.app import core

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),    
    url(r'^', include("kii.urls", namespace="kii")),
)
