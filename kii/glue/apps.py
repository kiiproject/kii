from kii.app import core


class App(core.App):
    name = "kii.glue"
    urls = ".urls"

    def get_url_prefix(self):
        return r'^$'