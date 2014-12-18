from django.utils.translation import ugettext_lazy as _

from kii.app import core, menu


class App(core.App):
    name = "kii.stream"
    urls = ".urls"
    user_access = True
    def ready(self):
        super(App, self).ready()
        self.menu = menu.MenuNode(
            route="kii:stream:index", 
            label=_("stream"),
            icon="fi-list",
            require_authentication=False,
            children = [
                menu.MenuNode(
                    route="kii:stream:stream:update",
                    label=_("update")
                )
            ]           
        )