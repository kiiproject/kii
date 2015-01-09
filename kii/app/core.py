"""
This module provides two core components for kii:

- :py:data:`apps`, an instance of :py:class:`AppManager`, used especialy for
   automatic URL inclusion of kii apps.
- :py:class:`App`, a class that extends django regular
  :py:class:`django.apps.AppConfig` and you should use for building your own \
   kii apps.
"""
from django.apps import AppConfig, apps as django_app_registry
from django.conf.urls import include, url
from django.core.urlresolvers import reverse


__all__ = ['App', 'AppManager']


class AppManager(object):
    """Provide a cleaner API to :py:data:`django.apps.apps`"""

    registry = django_app_registry

    def get(self, app_label):
        """
        :param str app_label:
        :return: A :py:class:`django.apps.AppConfig` instance corresponding to\
        the given app_abel.
        """
        return self.registry.get_app_config(app_label)

    def filter(self, **kwargs):
        """
        :return: an iterable of installed apps that match given filters"""

        filtered = []

        for app in self.all():
            match = True
            for attr, value in kwargs.items():
                if not hasattr(app, attr) or getattr(app, attr) != value:
                    match = False
                    break

            if match:
                filtered.append(app)

        return filtered

    def all(self):
        """:return: An iterable containing all the registered app configs"""
        return self.registry.get_app_configs()

    def kii_apps(self):
        """
        :return: An iterable containing all registered django apps marked that\
        are also kii apps
        """
        return self.filter(kii_app=True)

    def get_apps_urls(self, urlconf="urls"):
        """
        Gather all URLs for kii apps so they can easily be included in
        a URLconf.

        :return: A list of django url patterns
        """

        urls = []

        for app in self.kii_apps():
            if getattr(app, urlconf, None) is not None:
                app_urls = include(
                    app.urlconf(getattr(app, urlconf, None)),
                    namespace=app.label, app_name=app.label
                )
                included_url = url(app.get_url_prefix(), app_urls)
                urls.append(included_url)
        return urls


apps = AppManager()


class App(AppConfig):
    """A base class for all kii apps"""

    #: wether the app should be considered as a kii app or not.
    kii_app = True

    urls = None
    """A string containing the path to the app URLconf (if any). This URLconf
    will then be automatically registered under the ``kii`` namespace with
    :py:meth:`AppManager.get_apps_urls()`.

    You can use an absolute path, such as ``your_app.subpackage.urls`` or a
    relative path, like ``.urls``. In the last case, a full path will be built
    using :py:attr:`name <App.name>`.
    """

    api_urls = None
    """See :py:attr:`urls <App.urls>` for more details: a string containing
    the path to an URLconf that contains API urls (if any). This URLconf will
    be included under the ``kii:api``
    namespace."""

    menu = None
    """If you attach a :py:class:`MenuNode <kii.app.menu.MenuNode>` instance
    here, the corresponding menu will be automatically built and included in
    templates.

    :py:meth:`App.ready()` is a good place for registering your menu."""

    @property
    def installed(self):
        """:return: a boolean that indicates if the app is marked as installed \
        by django"""

        return apps.registry.is_installed(self.name)

    def get_url_prefix(self):
        """Return a prefix for used for URLconf inclusion, such as
        ``r'^myapp/'``. It must be a raw string, starting with ``^``
        and ending with a trailing slash.

        By default, uses the :py:attr:`label <App.label>` as the prefix."""

        return r'^{0}/'.format(self.label)

    def urlconf(self, target):
        """:param str target: The targeted path
        :return: The full path to the targeted URLconf, for further inclusion\
        in a URL pattern
        """

        # it's a realative URLconf, append it to app.name
        if target.startswith('.'):
            return self.name + target

        return target

    def public_models(self):
        """return a list of models from this app that can be created by
        any user
        TODO: is this used ?
        """

        return [model for model in self.get_models()
                if getattr(model, "public_model", False)]

    @property
    def index(self):
        """:return: A URL pointing to the app index"""
        return reverse("kii:{0}:index".format(self.label))
