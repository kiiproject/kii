from django.utils.translation import ugettext_lazy as _

from kii.app import core, menu


class App(core.App):
    name = "kii.stream"
    urls = ".urls"
    api_urls = ".api_urls"

    user_access = True
