from django.conf import settings
from django.contrib.auth.models import Group


def get_kii_users_group():
    """:return: the :py:class:`Group` instance that keep a reference
    to all kii users
    """

    return Group.objects.get(name=settings.ALL_USERS_GROUP)
