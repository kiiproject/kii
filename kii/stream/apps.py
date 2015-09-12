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

        registry.register(self.get_model("Stream"))
        registry.register(self.get_model("ItemComment"))
        registry.register(self.get_model("StreamItem"))

    def get_url_prefix(self):
        return r'^'
