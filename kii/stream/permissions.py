from rest_framework import permissions


class IsCommentModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Return `True` if `request.user` is owner of object's subject,
        `False` otherwise.
        """
        return obj.subject.owner == request.user
