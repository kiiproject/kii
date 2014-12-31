from . import core


def user_apps(request):
    """TODO : is user_access really needed ?"""
    return {'user_apps': core.apps.filter(user_access=True)}
