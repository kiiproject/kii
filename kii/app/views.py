from django.core.urlresolvers import resolve, reverse
from django.utils.encoding import force_text

from .core import apps


class AppMixin(object):
    """Add extra method and context to all apps views"""

    #: a page title that will be display in templates and ``<title>`` tags
    page_title = ""

    def setup(self, request, *args, **kwargs):
        """Called at the beginning of :py:meth:`dispatch`, you can extend this method
        if you need to set some variables for later use"""

        self.kwargs = kwargs
        self.args = args        
        self.request = request
        
    def pre_dispatch(self, request, *args, **kwargs):
        """Called just after :py:meth:`setup`. If you return anything but ``None``, the view 
        will stop and return the returned value.

        This method is convenient for checking a permission, for example.

        :return: None"""

        self.app = apps.get(request.resolver_match.app_name)

    def get_page_title(self):
        """Override this method if you want to return a custom title for the page.
        :return: A page title, as a string"""
        return self.page_title

    def dispatch(self, request, *args, **kwargs):
        """Set up some hooks before calling the actual dispatch method"""

        self.setup(request, *args, **kwargs)

        response = self.pre_dispatch(request, *args, **kwargs)
        if response is not None:
            return response

        return super(AppMixin, self).dispatch(request, *args, **kwargs)

    def get_title_components(self):
        """
        :return: an iterable of title elements , such as ``('Delete', 'My model', 'My app')`` \
        for use in templates. By default, returns only the app name.
        """
        return (self.app.verbose_name,)

    def get_context_data(self, **kwargs):
        """Add the current app, the page title, the title components and the root URL of kii to context"""
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