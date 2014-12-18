from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from kii.app import core

kii_urls = core.apps.get_apps_urls()
kii_api_urls = core.apps.get_apps_urls("api_urls")

urlpatterns = patterns('', 
    url(r'^api/', include(kii_api_urls, namespace="api")),
    url(r'^(?P<username>\w+)/', include(kii_urls, namespace="user_area")),
    url(r'^', include(kii_urls)),
    url(r'^$', RedirectView.as_view(url=reverse_lazy("kii:stream:index"), permanent=False)),
)
