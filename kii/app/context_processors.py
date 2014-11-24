from . import core

def user_apps(request):    
    return {'user_apps': core.apps.filter(user_access=True)}