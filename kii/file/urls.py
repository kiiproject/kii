from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from . import models, views, forms
from kii.stream import views as stream_views

file_patterns = patterns('',
    
    url(r'^$', views.FileList.as_view(), name='list'),
    url(r'^create$', stream_views.Create.as_view(form_class=forms.FileForm), name='create'),
    url(r'^(?P<pk>\d+)/update$', stream_views.Update.as_view(form_class=forms.FileForm), name='update'),
    url(r'^(?P<slug>[\w-]+)/update$', stream_views.Update.as_view(form_class=forms.FileForm), name='update'),
    url(r'^(?P<slug>[\w-]+)$', stream_views.Detail.as_view(model=models.File), name='detail'),
)

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=reverse_lazy("kii:file:file:list"), permanent=False), name="index"),    
    url(r'^', include(file_patterns, namespace='file', app_name='file')),
)