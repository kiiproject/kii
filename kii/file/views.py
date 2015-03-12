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

    path = f.file_obj.path
    filename = os.path.basename(path)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(path, 'rb'), chunk_size),
                           content_type=mimetypes.guess_type(path)[0])
    response['Content-Length'] = os.path.getsize(path)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
