from django.db import models
from django.core.urlresolvers import reverse

from kii import permission, utils, base_models

class PermissionModel(permission.models.PermissionMixin):
    
    def reverse_detail(self, **kwargs):
        return reverse("kii:user_area:test_permission:permissionmodel:detail", kwargs={"pk":self.pk, "username": self.owner.username})



class InheritPermissionModel(permission.models.InheritPermissionMixin):

    root = models.ForeignKey(PermissionModel, related_name="children")


class InheritInheritPermissionQuerySet(permission.models.InheritPermissionMixinQueryset):
    pass

class InheritInheritPermissionModel(permission.models.InheritPermissionMixin):
    objects = InheritInheritPermissionQuerySet.as_manager()
    root = models.ForeignKey(InheritPermissionModel, related_name="children")
    