import mimetypes
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from kii.stream.models import StreamItem


class File(StreamItem):

    file_obj = models.FileField(upload_to="kii/file/%Y/%m/%d")
    mimetype = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):

        self.mimetype = mimetypes.guess_type(self.file_obj.path)[0] or 'text/plain'
        super(File, self).save(*args, **kwargs)

    def reverse_raw(self, **kwargs):
        return reverse("kii:file:file:raw",
                       kwargs={"pk": self.pk})

    def type(self):
        return self.mimetype.split('/')[0]

    def subtype(self):
        return self.mimetype.split('/')[0]