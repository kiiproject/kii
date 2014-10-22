from kii.base_models import views
from . import models

class OwnerModelList(views.OwnerMixin, views.List):
    model = models.OwnerModel