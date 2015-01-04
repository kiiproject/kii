from django.utils.translation import ugettext_lazy as _

from kii.app import core, menu


class App(core.App):
    name = "kii.discussion"
    user_access = True

    def ready(self):
        super(App, self).ready()
        self.menu = menu.MenuNode(
            route="kii:stream:stream:itemcomment:list",
            label=_("discussion"),
            icon="fi-comments",
            require_authentication=False,
            reverse_kwargs=["stream"],
            children=[
                menu.MenuNode(
                    route="kii:stream:stream:itemcomment:moderation",
                    label=_("moderation"),
                    reverse_kwargs=["stream"],
                )
            ]
        )
