from __future__ import unicode_literals

from django.core.files.uploadedfile import SimpleUploadedFile
from kii.stream.tests.base import StreamTestCase

from .. import models


class TestFile(StreamTestCase):

    def test_file_accepts_uploaded_file(self):
        item = models.File(root=self.streams[0], title="Hello !")
        item.file_obj = SimpleUploadedFile('hello.txt', b'hello world!')

        item.save()

    def test_file_store_mimetype(self):
        item = models.File(root=self.streams[0], title="Hello !")
        item.file_obj = SimpleUploadedFile('hello.png', b'')

        item.save()

        self.assertEqual(item.mimetype, "image/png")
