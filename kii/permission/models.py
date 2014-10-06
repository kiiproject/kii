from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign
from django.conf import settings
from kii import base_models, user
from django.db import models
from guardian.shortcuts import get_objects_for_user, get_anonymous_user
from guardian.core import ObjectPermissionChecker

class PermissionMixinQuerySet(base_models.models.OwnerMixinQuerySet):

    def filter_permission(self, permissions, target):
        """Generic filter for permission. Rather low-level, you should use readable/writable/deletable_by instead"""

        matching = readable = get_objects_for_user(
            perms=permissions, klass=self, user=target, any_perm=True)

        # owned items are always accessible
        owned = self.owned_by(target)

        return matching | owned

    def readable_by(self, target):
        """Return objects readable by target (i.e. if the target has read, write or delete perm on them)"""        

        return self.filter_permission(["read", 'write', 'delete'], target)


class PermissionMixin(base_models.models.OwnerMixin):
    """Add some utility methods to retrieve permissions. Target always designate a Group or a User instance"""

    class Meta:
        abstract = True
        permissions = (
            ('read', _('permissions.view')),
            ('write', _('permissions.edit')),
            ('delete', _('permissions.delete')),
        )

    objects = PermissionMixinQuerySet.as_manager()

    def permission(self, permission, target):
        # owner has ALL permissions
        try:
            if target.pk == self.owner.pk:
                return True
        except AttributeError:
            pass

        checker = ObjectPermissionChecker(target)
        return checker.has_perm(permission, self)

    def readable_by(self, target):
        """Return True if given target has `read`, `edit` or `delete` permission on instance"""
        return self.writable_by(target) or self.permission("read", target)

    def writable_by(self, target):
        """Return True if given target has `write` or `delete` permission on instance"""
        return self.deletable_by(target) or self.permission("write", target)

    def deletable_by(self, target):
        """Return True if given target has `delete` permission on instance"""
        return self.permission("delete", target)

    def assign_perm(self, permission, target):
        """This method is not a shortcut but adds custom logic to guardian `assign`, so you have to use it"""

        if target.pk == get_anonymous_user().pk:
            # add also permission to all_users_group
            assign(permission, user.models.get_all_users_group(), self)

        return assign(permission, target, self)


class InheritPermissionMixinQueryset(PermissionMixinQuerySet):
    
    def filter_permission(self, permissions, target):
        matching = super(InheritPermissionMixinQueryset, self).filter_permission(permissions, target)


        # get parent field and class for filtering
        parent_field = [field for field in self.model._meta.fields if field.name == self.inherit_permissions_target][0]
        parent_class = parent_field.rel.to

        # grab parent IDS corresponding to given permission
        filters = {"{0}__inherit_permissions".format(self.inherit_permissions_related_name):True}
        parents = parent_class.objects.filter_permission(permissions, target).filter(**filters).distinct().values('id')

        parent_ids = [parent['id'] for parent in parents]

        # query inheriting models using these ids
        filters = {
            "{0}__pk__in".format(self.inherit_permissions_target):parent_ids, 
            "inherit_permissions": True
        }
        inheriting = self.filter(**filters)

        return matching | inheriting



class InheritPermissionMixin(PermissionMixin):

    objects = InheritPermissionMixinQueryset.as_manager()
    Meta = PermissionMixin.Meta

    def permission(self, permission, target):
        if self.inherit_permissions:
            return getattr(self, self.inherit_permissions_from).permission(permission, target)

        return super(InheritPermissionMixin, self).permission(permission, target)

def get_inherit_permission_model(model_name, target="parent", related_name="children"):
    """Return a model class that can will inherit permissions from parent field"""


    class QS(InheritPermissionMixinQueryset):
        inherit_permissions_target = target
        inherit_permissions_related_name = related_name

    Model = type(
        str('InheritPermissionMixin_{0}'.format(model_name)), 
        (InheritPermissionMixin,), 
        {
            str('inherit_permissions'): models.BooleanField(default=True),
            str('inherit_permissions_from'): target,
            str('Meta'): PermissionMixin.Meta,
            str('__module__'): __name__,
        })


    return Model, QS.as_manager()


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

    def readable_by(self, user):
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


def remove_obj_perms(sender, instance, **kwargs):
    filters = Q(content_type=ContentType.objects.get_for_model(instance),
        object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()

pre_delete.connect(remove_obj_perms)