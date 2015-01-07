from django.contrib.auth import get_user_model
from actstream import registry

from kii.app import core


class App(core.App):
    name = "kii.user"
    urls = ".urls"

    def ready(self):
        registry.register(get_user_model())
