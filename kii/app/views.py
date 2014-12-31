from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from .core import apps


class AppMixin(object):
    """Add extra method and context to all apps views"""

    #: a page title that will be display in templates and ``<title>`` tags
    page_title = ""

    def setup(self, request, *args, **kwargs):
        """Called at the beginning of :py:meth:`dispatch`, you can extend
        this method
        if you need to set some variables for later use"""

        self.kwargs = kwargs
        self.args = args
        self.request = request

    def pre_dispatch(self, request, *args, **kwargs):
        """Called just after :py:meth:`setup`. If you return anything but
        ``None``, the view will stop and return the returned value.

        This method is convenient for checking a permission, for example.

        :return: None"""

        self.app = apps.get(request.resolver_match.app_name)

    def get_page_title(self):
        """Override this method if you want to return a custom title for
        the page.
        :return: A page title, as a string"""
        return self.page_title

    def dispatch(self, request, *args, **kwargs):
        """Set up some hooks before calling the actual dispatch method"""

        self.setup(request, *args, **kwargs)

        response = self.pre_dispatch(request, *args, **kwargs)
        if response is not None:
            return response

        return super(AppMixin, self).dispatch(request, *args, **kwargs)

    def get_breadcrumbs(self):
        """:return: an tuple of breadcrumb elements , such as
        ``(('Delete' '/delete'), ('My model', None), ('My app', None))``
        for use in templates. The first item of each tuple is the title of
        the element, the second is the URL. URL can be None.
        """
        return ((self.app.verbose_name, None),)

    def get_context_data(self, **kwargs):
        """Add the current app, the page title, the breadcrumbs and the
        root URL of kii to context
        """
        context = super(AppMixin, self).get_context_data(**kwargs)

        context['app'] = self.app

        breadcrumbs = [
            (force_text(title, ), url)
            for title, url in self.get_breadcrumbs()
            if force_text(title)
        ]

        page_title = self.get_page_title()
        if page_title:
            breadcrumbs += ((force_text(page_title), None),)
            context['page_title'] = page_title

        context['breadcrumbs'] = breadcrumbs
        context['full_title'] = " | ".join(
            reversed([title for title, url in breadcrumbs])
        )

        context['kii_root'] = self.request.build_absolute_uri(
            reverse('kii:glue:home')
        )

        return context
