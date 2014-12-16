from kii.base_models import views
from django.http import Http404



class RequirePermissionMixin(views.RequireBasePermissionMixin):

    def has_required_permission(self, user):        
        mapping = {
            "read": "readable_by",
            "write": "writable_by",
            "delete": "deletable_by",
        } 
        checker = getattr(self.object, mapping[self.required_permission])
        return checker(user)


class PermissionMixinDetail(RequirePermissionMixin, views.OwnerMixinDetail):
    required_permission = "read"


class PermissionMixinUpdate(RequirePermissionMixin, views.OwnerMixinUpdate):
    required_permission = "write"


class PermissionMixinDelete(RequirePermissionMixin, views.OwnerMixinDelete):
    required_permission = "delete"
       

class PermissionMixinList(RequirePermissionMixin, views.OwnerMixinList):
    """Filter model instances depending on user and permissions"""

    def get_queryset(self):

        # retrieve standard queryset
        queryset = super(PermissionMixinList, self).get_queryset()

        return queryset.readable_by(self.request.user.pk)
        

class PrivateReadDetail(PermissionMixinDetail):
    pass

class PrivateReadList(PermissionMixinList):
    pass

            