from django.http import Http404, HttpResponse
from kii.stream import views

from . import models


class FileList(views.List):
    streamitem_class = models.File


def FileRaw(request, **kwargs):

    try:
        f = models.File.objects.get(pk=kwargs.get('pk'))
    except models.File.DoesNotExist:
        raise Http404

    if not f.readable_by(request.user):
        raise Http404

    extension = f.name.split('.')[-1]
    content = f.file_obj.read()
    response = HttpResponse(content, content_type=f.mimetype)
    response['Content-Disposition'] = "attachment; filename=\"{0}.{1}\"".format(
        f.root.title, f.title, extension
        )
    return response