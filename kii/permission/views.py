from kii.base_models import views


class SingleObjectRequirePermissionMixin(views.SingleObjectPermissionMixin):

    def has_required_permission(self, request, *args, **kwargs):
        mapping = {
            "read": "readable_by",
            "write": "writable_by",
            "delete": "deletable_by",
        }
        checker = getattr(self.object, mapping[self.required_permission])
        return checker(request.user)


class PermissionMixinDetail(SingleObjectRequirePermissionMixin,
                            views.OwnerMixinDetail):
    required_permission = "read"


class PermissionMixinUpdate(SingleObjectRequirePermissionMixin,
                            views.OwnerMixinUpdate):
    required_permission = "write"


class PermissionMixinDelete(SingleObjectRequirePermissionMixin,
                            views.OwnerMixinDelete):
    required_permission = "delete"


class PermissionMixinList(views.MultipleObjectPermissionMixin,
                          views.OwnerMixinList):
    """Filter model instances depending on user and permissions"""

    def get_queryset(self):

        # retrieve standard queryset
        queryset = super(PermissionMixinList, self).get_queryset()

        return queryset.readable_by(self.request.user)


class PrivateReadDetail(PermissionMixinDetail):
    pass


class PrivateReadList(PermissionMixinList):
    pass
