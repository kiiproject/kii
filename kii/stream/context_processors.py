from . import models


def user_stream(request):
    """Added request user stream to context"""
    if request.user.is_authenticated():
        return {'user_stream': models.Stream.objects.get_user_stream(request.user)}
    return {}
