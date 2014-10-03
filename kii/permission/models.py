from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign
from django.conf import settings
from kii import base_models
from django.db import models
from guardian.shortcuts import get_objects_for_user

class PermissionMixinQuerySet(base_models.models.OwnerMixinQuerySet):

    def readable_by(self, user):
        """Return objects readable by user (i.e. if the user has read, write or delete perm on them)"""
        
        readable = get_objects_for_user(
            perms=["read", 'write', 'delete'], klass=self, user=user, any_perm=True)
        return readable

class PermissionMixin(base_models.models.OwnerMixin):
    """Add some utility methods to retrieve permissions"""

    class Meta:
        abstract = True
        permissions = (
            ('read', _('permissions.view')),
            ('write', _('permissions.edit')),
            ('delete', _('permissions.delete')),
        )

    objects = PermissionMixinQuerySet.as_manager()

    def permission(self, permission, user):
        # owner has ALL permissions
        if user.pk == self.owner.pk:
            return True

        return user.has_perm(permission, self)

    def readable_by(self, user):
        """Return True if given user has `read`, `edit` or `delete` permission on instance"""
        return self.writable_by(user) or self.permission("read", user)

    def writable_by(self, user):
        """Return True if given user has `write` or `delete` permission on instance"""
        return self.deletable_by(user) or self.permission("write", user)

    def deletable_by(self, user):
        """Return True if given user has `delete` permission on instance"""
        return self.permission("delete", user)

    def assign_perm(self, permission, user):
        return assign(permission, user, self)


class PrivateReadMixinQuerySet(PermissionMixinQuerySet):

    def readable_by(self, user):

        has_read_permissions = super(PrivateReadMixinQuerySet, self).readable_by(user)
        readable = self.filter(read_private=False)
        return readable | has_read_permissions


class PrivateReadMixin(PermissionMixin):
    """Model inheriting from this mixin will have a public/private setting for viewing (not writing)"""
    
    read_private = models.BooleanField(_('base_models.privatereadmixin.read_private'), default=True)

    objects = PrivateReadMixinQuerySet.as_manager()

    class Meta(PermissionMixin.Meta):
        abstract = True

    def readable(self, user):
        if not self.read_private:
            return True
        # return value from PermissionMixin
        return super(PrivateReadMixin, self).readable_by(user)

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