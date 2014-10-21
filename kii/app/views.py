from django.core.urlresolvers import resolve
from .core import apps


class AppMixin(object):
    """Add extra context to all apps views"""

    def dispatch(self, request, *args, **kwargs):

        self.app = apps.get(request.resolver_match.app_name)
        return super(AppMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super(AppMixin, self).get_context_data()

        context['app'] = self.app
        
        return context