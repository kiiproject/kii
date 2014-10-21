from kii import base_models
from django.db import models
from kii.base_models import fields

class TitleModel(base_models.models.TitleMixin):
    pass


class TitleModel2(TitleModel):
    pass

class OwnerModel(base_models.models.OwnerMixin):
    useless_field = models.CharField(max_length=255, default="", blank=True)


InheritModel, signals = base_models.models.get_inherit_model(
    local_field='title', 
    target="parent",
    target_class=TitleModel,
    target_related_name="yolo")

class InheritTitleModel(InheritModel, base_models.models.TitleMixin):

    parent = models.ForeignKey(TitleModel, related_name="yolo")

from django.db.models.signals import pre_save, post_save

pre_save.connect(signals['pre_save'])
post_save.connect(signals['post_save'])


class StatusModel(base_models.models.StatusMixin):

    pass


class ContentModel(base_models.models.ContentMixin):

    pass

class SlugModel(base_models.models.TitleMixin):
    slug = fields.SlugField(populate_from=("title",))

class TimestampModel(base_models.models.TimestampMixin):

    pass