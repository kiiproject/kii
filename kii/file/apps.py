from django.utils.translation import ugettext_lazy as _
from kii.app import core, menu



class App(core.App):
    name = "kii.file"
    urls = ".urls"
    user_access = True
    
    def ready(self):
        super(App, self).ready()
        self.menu = menu.MenuNode(
            route="kii:file:index", 
            label=_("files"),
            icon="fi-folder",
            children = [
                menu.MenuNode(
                    route="kii:file:file:create",
                    label=_("create")
                )
            ]           
    )