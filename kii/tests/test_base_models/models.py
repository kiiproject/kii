from kii import base_models
from django.db import models


class NameModel(base_models.models.NameMixin):
    pass

class OwnerModel(base_models.models.OwnerMixin):
    useless_field = models.CharField(max_length=255, default="", blank=True)


InheritModel, signals = base_models.models.get_inherit_model(
    local_field='name', 
    target="parent",
    target_class=NameModel,
    target_related_name="yolo")

class InheritNameModel(InheritModel, base_models.models.NameMixin):

    parent = models.ForeignKey(NameModel, related_name="yolo")

from django.db.models.signals import pre_save, post_save

pre_save.connect(signals['pre_save'])
post_save.connect(signals['post_save'])

