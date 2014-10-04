from kii import permission

class PermissionModel(permission.models.PermissionMixin):
    pass

class PrivateReadModel(permission.models.PrivateReadMixin):
    pass