from django.conf.urls import patterns, url
from . import views

from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^login$', views.login, name="login"), # NOQA
    url(r'^logout$', views.logout, {'next_page': '/'}, name="logout"),
    url(r'^profile$', TemplateView.as_view(template_name="glue/home.html"), name="profile"),
)
