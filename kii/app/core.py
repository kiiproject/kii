from django.apps import AppConfig, apps as django_app_registry



class AppQueryset(object):
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

apps = AppQueryset()


class App(AppConfig):
    """A base class for all Kii apps"""

    kii_app = True

    @property
    def installed(self):
        return apps.registry.is_installed(self.name)
