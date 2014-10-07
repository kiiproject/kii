from kii import permission, utils, base_models
from django.db import models

class PermissionModel(permission.models.PermissionMixin):
    pass



class InheritPermissionModel(permission.models.InheritPermissionMixin):

    parent = models.ForeignKey(PermissionModel, related_name="children")


class InheritInheritPermissionQuerySet(permission.models.InheritPermissionMixinQueryset):
    pass

class InheritInheritPermissionModel(permission.models.InheritPermissionMixin):
    objects = InheritInheritPermissionQuerySet.as_manager()
    parent = models.ForeignKey(InheritPermissionModel, related_name="children")
    