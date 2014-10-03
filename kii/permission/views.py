from kii.base_models import views
from django.http import Http404
from django.contrib.auth import get_user
from guardian.shortcuts import get_objects_for_user

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

        # first get object with explicit read permission
        readable = get_objects_for_user(perms="read", klass=self.model, user=self.request.user)

        # retrieve standard queryset
        qs = super(PermissionMixinList, self).get_queryset()

        # owned elements
        owned = qs.filter(owner=self.request.user.pk)

        return readable | owned
        

class PrivateReadList(PermissionMixinList):

    def get_queryset(self):
        
        qs = super(PrivateReadList, self).get_queryset()

        # public elements
        public = self.model.objects.filter(read_private=False)
        return qs | public 



            