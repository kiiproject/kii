import registries

class App:

    #: A registry of app models
    #: 
    models = {}

    def __init__(self, *args, **kwargs):

        self.models = registries.ModelRegistry()