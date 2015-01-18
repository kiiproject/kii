from django.utils.translation import ugettext_lazy as _
from kii.app import core, menu



class App(core.App):
    name = "kii.file"

    user_access = True
