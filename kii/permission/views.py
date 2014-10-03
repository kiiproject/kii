from kii.base_models import views
from django.http import Http404
from django.contrib.auth import get_user

class PrivateReadDetail(views.Detail):
    """Raise 404 when unauthorized user try to detail a private model instance"""

    def get_object(self, queryset=None):
        obj = super(PrivateReadDetail, self).get_object(queryset)

        if not obj.readable(self.request.user):
            raise Http404

        return obj



            