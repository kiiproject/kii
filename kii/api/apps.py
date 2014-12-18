from django.utils.translation import ugettext_lazy as _

from kii.app import core


class App(core.App):
    name = "kii.api"
    label = "api"