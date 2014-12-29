from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class OwnerMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.owner = self.get_owner(request, view_kwargs)

    def get_owner(self, request, view_kwargs):
        owner_name = view_kwargs.get('username', None)
        if owner_name is None:
            if request.user.is_authenticated():
                return request.user
            elif getattr(settings, "KII_DEFAULT_USER", None) is not None:
                return User.objects.get(username=getattr(settings, "KII_DEFAULT_USER"))

            else:
                return None
        else:
            return User.objects.get(username=owner_name)
