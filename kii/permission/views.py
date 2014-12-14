from kii.base_models import views
from django.http import Http404



class RequirePermissionMixin(object):

    permission_denied = Http404

    def get_object(self, **kwargs):
        obj = super(RequirePermissionMixin, self).get_object(**kwargs)
        if not self.has_required_permission(obj, self.request.user):
            raise self.permission_denied
        return obj

    def has_required_permission(self, obj, user):        
        mapping = {
            "read": "readable_by",
            "write": "writable_by",
            "delete": "deletable_by",
        } 
        checker = getattr(obj, mapping[self.required_permission])
        return checker(user)


class PermissionMixinDetail(RequirePermissionMixin, views.OwnerMixinDetail):
    """Raise 404 when unauthorized user try to detail a private model instance"""

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

            