from django.core.urlresolvers import resolve, reverse
from .core import apps


class AppMixin(object):
    """Add extra context to all apps views"""

    def dispatch(self, request, *args, **kwargs):

        self.app = apps.get(request.resolver_match.app_name)
        return super(AppMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AppMixin, self).get_context_data(**kwargs)

        context['app'] = self.app
        context['kii_root'] = self.request.build_absolute_uri(reverse('kii:glue:home'))
        return context