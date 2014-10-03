from kii.base_models import views
from django.http import Http404

class PrivateReadDetail(views.Detail):
    """Raise 404 when unauthorized user try to detail a private model instance"""

    def get_object(self, queryset=None):
        obj = super(PrivateReadDetail, self).get_object(queryset)

        if not obj.readable(self.request.user):
            raise Http404

        return obj


class PermissionMixinList(views.List):
    """Filter model instances depending on user and permissions"""

    def get_queryset(self):

        # retrieve standard queryset
        queryset = super(PermissionMixinList, self).get_queryset()

        return queryset.readable_by(self.request.user.pk)
        

class PrivateReadList(PermissionMixinList):

    pass

            