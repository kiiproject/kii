from django.conf.urls import patterns, url, include
from .. import views
from django.views.generic import TemplateView
from .views import Home

urlpatterns = patterns('',
     url(r'^hello', views.blank, name='index'),
     url(r'^home', Home.as_view(template_name="test_app/home.html"), name='home'),
)
