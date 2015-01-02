from django.utils.translation import ugettext_lazy as _
from actstream import registry
from kii.app import core, menu

from . import models


class App(core.App):
    name = "kii.stream"
    urls = ".urls"
    api_urls = ".api_urls"

    user_access = True

    def ready(self):
        registry.register(models.Stream)
        registry.register(models.ItemComment)
        registry.register(models.StreamItem)
