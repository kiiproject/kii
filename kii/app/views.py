from django.core.urlresolvers import resolve, reverse
from django.utils.encoding import force_text

from .core import apps


class AppMixin(object):
    """Add extra context to all apps views"""

    page_title = ""

    def setup(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args        
        self.request = request
        
    def pre_dispatch(self, request, *args, **kwargs):
        
        self.app = apps.get(request.resolver_match.app_name)

    def get_page_title(self):
        return self.page_title

    def dispatch(self, request, *args, **kwargs):
        
        self.setup(request, *args, **kwargs)

        response = self.pre_dispatch(request, *args, **kwargs)
        if response is not None:
            return response

        return super(AppMixin, self).dispatch(request, *args, **kwargs)

    def get_title_components(self):
        return (self.app.verbose_name,)

    def get_context_data(self, **kwargs):
        context = super(AppMixin, self).get_context_data(**kwargs)

        context['app'] = self.app
        title_components = [force_text(component) for component in self.get_title_components() if force_text(component)]
        page_title = self.get_page_title()
        if page_title:
            title_components.insert(0, force_text(page_title))
            context['page_title'] = page_title

        context['title_components'] = title_components        
        context['full_title'] = " | ".join(title_components)

        context['kii_root'] = self.request.build_absolute_uri(reverse('kii:glue:home'))

        return context