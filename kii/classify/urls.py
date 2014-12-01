from django.conf.urls import patterns, url, include
from kii.base_models import views
from . import forms, models

tag_patterns = patterns('',
     url(r'^create$', views.OwnerMixinCreate.as_view(form_class=forms.TagForm), name='create'),
     url(r'^(?P<pk>\d+)/$', views.OwnerMixinDetail.as_view(model=models.Tag), name='detail'),
)

urlpatterns = patterns('',
     url(r'^tag/', include(tag_patterns, namespace="tag")),
)