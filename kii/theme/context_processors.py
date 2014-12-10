from django.conf import settings

def user_apps(request):    
    return {'kii_theme': settings.KII_THEME}