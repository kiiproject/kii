from django.conf.urls import patterns, url, include
from . import views

autocomplete_patterns = [
    url(r'^navigation$', views.NavigationAutocomplete, name="navigation"),
]
urlpatterns = patterns('',
    url(r'^autocomplete/', include(autocomplete_patterns, namespace="autocomplete"))
)
