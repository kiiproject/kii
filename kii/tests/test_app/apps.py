from kii.app import core, menu

class App(core.App):
    name = "kii.tests.test_app"
    urls = ".urls"
    verbose_name = "Test app"

    def ready(self):
        self.menu = menu.MenuNode(
            route="kii:test_app:index", 
            label="Test App Index", 
            title="Click to return home",
            children = [
                menu.MenuNode(
                    route="kii:test_app:first",
                    weight=100,
                ),
                menu.MenuNode(
                    route="kii:test_app:third",
                    weight=80,
                ),
                menu.MenuNode(
                    route="kii:test_app:second",
                    weight=90,
                ),
            ]
        )

