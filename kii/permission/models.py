from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign
from django.conf import settings
from kii import base_models
from django.db import models

class PermissionMixin(base_models.models.OwnerMixin):
    """Add some utility methods to retrieve permissions"""

    class Meta:
        abstract = True
        permissions = (
            ('view', _('permissions.view')),
            ('edit', _('permissions.edit')),
            ('delete', _('permissions.delete')),
        )

    def permission(self, permission, user):
        # owner has ALL permissions
        if user is self.owner:
            return True

        return user.has_perm(permission, self)

    def viewable(self, user):
        """Return True if given user has `view`, `edit` or `delete` permission on instance"""

        return self.editable(user) or self.permission("view", user)

    def editable(self, user):
        """Return True if given user has `edit` or `delete` permission on instance"""
        return self.deletable(user) or self.permission("edit", user)

    def deletable(self, user):
        """Return True if given user has `delete` permission on instance"""
        return self.permission("delete", user)

    def assign_perm(self, permission, user):
        return assign(permission, user, self)

class PrivateViewMixin(PermissionMixin):
    """Model inheriting from this mixin will have a public/private setting for viewing (not writing)"""
    
    view_private = models.BooleanField(_('base_models.privateviewmixin.view_private'), default=True)

    class Meta:
        abstract = True

    def viewable(self, user):
        """return True if given user can view the model instance"""
        if not self.view_private:
            return True
        # return value from PermissionMixin
        return super(PrivateViewMixin, self).viewable(user)

# automatic deletion of permission when a user is deleted
# from http://django-guardian.readthedocs.org/en/latest/userguide/caveats.html
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_delete
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission


def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    filters = Q(content_type=ContentType.objects.get_for_model(instance),
        object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()

pre_delete.connect(remove_obj_perms_connected_with_user, sender=settings.AUTH_USER_MODEL)