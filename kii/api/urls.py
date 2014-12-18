from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView

from kii.app import core

kii_api_urls = core.apps.get_apps_urls("api_urls")
urlpatterns = patterns('', 
    url(r'^api/', include(kii_api_urls, namespace="api")),
)

print(urlpatterns, kii_api_urls)