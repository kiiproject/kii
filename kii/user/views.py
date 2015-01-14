from django.contrib.auth import views
from django.contrib import messages

from kii.stream.models import Stream

def login(request, **kwargs):
    r = views.login(request, **kwargs)
    if request.user.is_authenticated():
        if not request.session.get('default_stream'):
            request.session['selected_stream'] = Stream.objects.get_user_stream(request.user).pk
        messages.success(request, "user.login.success")
    return r


def logout(request, **kwargs):
    return views.logout(request, **kwargs)
