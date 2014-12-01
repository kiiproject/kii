from django.contrib.auth import views
from django.contrib import messages


def login(request, **kwargs):
    r = views.login(request, **kwargs)
    if request.user.is_authenticated():
        messages.success(request, "user.login.success")
    return r

def logout(request, **kwargs):
    return views.logout(request, **kwargs)