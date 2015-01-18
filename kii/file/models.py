import mimetypes
from django.db import models

from kii.stream.models import StreamItem


class File(StreamItem):

    file_obj = models.FileField(upload_to="kii/file/%Y/%m/%d")
    mimetype = models.CharField(max_length=255)

    def save(self, *args, **kwargs):

        self.mimetype = mimetypes.guess_type(self.file_obj.path)[0] or 'text/plain'
        super(File, self).save(*args, **kwargs)