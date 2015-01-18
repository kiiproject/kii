from kii.stream import views

from . import models


class FileList(views.List):
    streamitem_class = models.File

