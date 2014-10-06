from kii import permission
from django.db import models


class PermissionModel(permission.models.PermissionMixin):
    pass

class PrivateReadModel(permission.models.PrivateReadMixin):
    pass



inherit_permission_model, manager = permission.models.get_inherit_permission_model(model_name="Ipm", target="parent", related_name="children")

class InheritPermissionModel(
    inherit_permission_model,
    permission.models.PermissionMixin):

    parent = models.ForeignKey(PermissionModel, related_name="children")
    objects = manager


for k, v in InheritPermissionModel._meta.fields[-1].rel.__dict__.items():
    print(k, v)