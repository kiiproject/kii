from kii.app import views
from django.views.generic import TemplateView


class Home(views.AppMixin, TemplateView):
    pass
