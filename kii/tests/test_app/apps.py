from kii.app import core, menu

class App(core.App):
    name = "kii.tests.test_app"
    urls = ".urls"
    verbose_name = "Test app"


    def ready(self):
        self.menu = menu.Menu(
            route="kii:test_app:index", 
            label="Test App Index", 
            title="Click to return home",
            children = [
                menu.MenuItem(
                    route="kii:test_app:first",
                    weight=100,

                ),
                menu.MenuItem(
                    route="kii:test_app:third",
                    weight=80,
                ),
                menu.MenuItem(
                    route="kii:test_app:second",
                    weight=90,
                ),
                menu.MenuItem(
                    route="kii_user:test_app:user",
                    weight=50,
                ),
            ]
        )

