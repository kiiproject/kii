from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm

from kii.app.core import apps

class Home(TemplateView):
    
    template_name = "glue/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm()
        context['user_apps'] = apps.filter(user_access=True)
        return context
