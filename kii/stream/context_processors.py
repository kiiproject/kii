from . import models


def user_stream(request):
    """Added request user stream to context"""
    if request.user.is_authenticated():
        return {'user_stream': models.Stream.objects.get_user_stream(request.user)}
    return {}


def item_models(request):
    """Added availble stream item subclasses"""
    return {
        'item_models': sorted(models.StreamItem.__subclasses__(), 
                              key=lambda x: x._meta.verbose_name)
    }
