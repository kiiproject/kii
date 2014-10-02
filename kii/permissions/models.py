from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign
import base_models

class PermissionMixin(base_models.models.BaseMixin):
    """Add some utility methods to retrieve permissions"""

    class Meta:
        abstract = True
        permissions = (
            ('view', _('permissions.view')),
            ('edit', _('permissions.edit')),
            ('delete', _('permissions.delete')),
        )

    def permission(self, permission, user):
        return user.has_perm(permission, self)

    def viewable(self, user):
        return self.permission("view", user)

    def editable(self, user):
        return self.permission("edit", user)

    def deletable(self, user):
        return self.permission("delete", user)

    def assign_perm(self, permission, user):
        assign(permission, user, self)
