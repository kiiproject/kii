from django.apps import AppConfig, apps as django_app_registry
from django.conf.urls import include, url

from . import menu



class AppManager(object):
    """Provide a cleaner API to django.apps.apps"""

    registry = django_app_registry

    def get(self, app_label):
        return self.registry.get_app_config(app_label)

    def filter(self, **kwargs):
        """Return an iterable of installed apps that match given filters"""
        
        filtered = []

        for app in self.all():
            match = True
            for attr, value in kwargs.items():
                if not hasattr(app, attr) or getattr(app, attr) != value :
                    match = False 
                    break   

            if match:
                filtered.append(app)

        return filtered

    def all(self):
        return self.registry.get_app_configs()

    def kii_apps(self):
        return self.filter(kii_app=True)

    def get_apps_urls(self):
        """Gather all URLs for kii apps and return them as a list, so they can easily be included
        in a root URLConf, for example"""

        urls = []

        for app in self.kii_apps():
            if app.urls is not None:
                included_url = url(app.get_url_prefix(), include(app.urlconf, namespace=app.label, app_name=app.label))
                urls.append(included_url)

        return urls

apps = AppManager()


class App(AppConfig):
    """A base class for all Kii apps"""

    kii_app = True

    # replace this with a urlconf module that would be automatically gathered 
    # by AppManager.get_apps_urls(), such as "your_app.urls"
    # if the string start with a dot, such as ".urls", a full path will be built by joining
    # app.name and app.urls
    urls = None


    menu = None

    @property
    def installed(self):
        return apps.registry.is_installed(self.name)

    def get_url_prefix(self):
        """return a prefix for incldugind the app URLconf, such as r'^myapp/'
        It must be a raw string, starting with `^` and ending with a trailing slash
        By default, uses the app label as a prefix"""
        return r'^{0}/'.format(self.label)

    @property
    def urlconf(self):
        """Return the full path to the app URLconf"""

        # it's a realative URLconf, append it to app.name
        if self.urls.startswith('.'):
            return self.name + self.urls

        return self.urls

    def public_models(self):
        """return a list of models from this app that can be created by any user
        """

        return [model for model in self.get_models() if getattr(model, "public_model", False)]
