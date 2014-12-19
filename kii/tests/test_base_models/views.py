from kii.base_models import views
from . import models, filterset

class OwnerModelList(views.OwnerMixin, views.List):
    model = models.OwnerModel


class StatusModelList(views.List):
    model = models.StatusModel
    filterset_class = filterset.StatusFilterSet