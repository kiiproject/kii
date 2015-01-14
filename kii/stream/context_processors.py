from . import models


def streams(request):
    """Add request user streams"""
    context = {}
    if request.user.is_authenticated():
        context['user_streams'] = models.Stream.objects.filter(owner=request.user)
        context['default_user_stream'] = context['user_streams'].first()
    return context


def stream_models(request):
    """Add availble stream item subclasses and stream model"""
    return {
        'item_models': sorted(models.StreamItem.__subclasses__(), 
                              key=lambda x: x._meta.verbose_name),
        'stream_model': models.Stream
    }
