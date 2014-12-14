from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign, remove_perm
from django.conf import settings
from django.db import models
from guardian.shortcuts import get_objects_for_user, get_anonymous_user
from guardian.core import ObjectPermissionChecker

from kii.base_models import models as base_models_models
from kii.user import models as user_models

class PermissionMixinQuerySet(base_models_models.OwnerMixinQuerySet):

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


class PermissionMixin(base_models_models.OwnerMixin):
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
            assign(permission, user_models.get_all_users_group(), self)

        return assign(permission, target, self)

    def remove_perm(self, permission, target):
        if target.pk == get_anonymous_user().pk:
            # add also remove all_user_group permission
            remove_perm(permission, get_anonymous_user(), self)
            remove_perm(permission, user_models.get_all_users_group(), self)

class InheritPermissionMixinQueryset(PermissionMixinQuerySet):
    
    def filter_permission(self, permissions, target):
        matching = super(InheritPermissionMixinQueryset, self).filter_permission(permissions, target)


        # get root field and class for filtering
        root_field = [field for field in self.model._meta.fields if field.name == "root"][0]
        root_class = root_field.rel.to

         # grab root IDS corresponding to given permission
        roots = root_class.objects.filter_permission(
            permissions, target).filter(children__inherit_permissions=True).distinct().values('id')

        root_ids = [root['id'] for root in roots]

        # query inheriting models using these ids
        filters = {
            "root__pk__in": root_ids, 
            "inherit_permissions": True
        }
        inheriting = self.filter(**filters)

        return matching | inheriting



class InheritPermissionMixin(PermissionMixin):

    objects = InheritPermissionMixinQueryset.as_manager()
    inherit_permissions = models.BooleanField(default=True)

    class Meta(PermissionMixin.Meta):
        abstract = True

    def permission(self, permission, target):
        if self.inherit_permissions:
            return self.root.permission(permission, target)

        return super(InheritPermissionMixin, self).permission(permission, target)

# automatic deletion of permission when a user is deleted
# from http://django-guardian.readthedocs.org/en/latest/userguide/caveats.html
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_delete, pre_save
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission


def remove_obj_perms(sender, instance, **kwargs):
    filters = Q(content_type=ContentType.objects.get_for_model(instance),
        object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()

pre_delete.connect(remove_obj_perms)



def set_inherit_permission_owner(sender, instance, **kwargs):
    if issubclass(sender, InheritPermissionMixin):
        instance.owner = instance.root.owner

pre_save.connect(set_inherit_permission_owner)