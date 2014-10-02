import persisting_theory

class ModelRegistry(persisting_theory.Registry):
    """A registry for storing app models"""

class AppRegistry(persisting_theory.Registry):
    """A registry for storing apps instances"""

app_registry = AppRegistry()