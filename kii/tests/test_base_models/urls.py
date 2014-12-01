from django.conf.urls import patterns, url, include
from kii.base_models import views
from . import models, forms
from .views import OwnerModelList

titlemodel_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.TitleModel), 
        name='detail'),
    url(r'$', 
        views.List.as_view(model=models.TitleModel), 
        name='list'),
)
titlemodel2_patterns = patterns('',
    url(r'^(?P<pk>\d+)/$', 
        views.Detail.as_view(model=models.TitleModel2), 
        name='detail'),
    url(r'^create$', 
        views.Create.as_view(model=models.TitleModel2), 
        name='create'),
    url(r'^$', 
        views.List.as_view(model=models.TitleModel2), 
        name='list'),
    url(r'^(?P<pk>\d+)/delete$', 
        views.Delete.as_view(model=models.TitleModel2), 
        name='delete'),
)

ownermodel_patterns = patterns('',
    url(r'^create$', 
        views.OwnerMixinCreate.as_view(
            form_class=forms.OwnerModelForm, 
            template_name="base_models/modelform.html",
            fields=['useless_field']), 
        name='create'),
    url(r'^$', 
        OwnerModelList.as_view(), 
        name='list'),
    url(r'^(?P<pk>\d+)/update$', 
        views.OwnerMixinUpdate.as_view(form_class=forms.OwnerModelForm,        
        template_name="base_models/modelform.html",
        fields=['useless_field']),  
        name='update'),
    url(r'^(?P<pk>\d+)/delete$', 
        views.OwnerMixinDelete.as_view(model=models.OwnerModel),  
        name='delete'),

)

urlpatterns = patterns('',
    url(
        r'^titlemodel/', 
        include(
            titlemodel_patterns, 
            namespace='titlemodel', 
            app_name='titlemodel')
        ),
    url(
        r'^titlemodel2/', 
        include(
            titlemodel2_patterns, 
            namespace='titlemodel2', 
            app_name='titlemodel2')
        ),
    url(
        r'^ownermodel/', 
        include(
            ownermodel_patterns, 
            namespace='ownermodel', 
            app_name='ownermodel')
        ),

)