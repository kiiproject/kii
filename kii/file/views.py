import mimetypes
import os
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper

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
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(f.file_obj.open(), chunk_size),
                           content_type=f.mimetype)
    response['Content-Disposition'] = "attachment; filename=\"{0}.{1}\"".format(
        f.root.title, f.title, extension
        )
    response['Content-Length'] = f.file_obj.size    
    return response

