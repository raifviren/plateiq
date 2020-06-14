"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update', 'partial_update'] and obj.id == request.user.id \
               or request.user.is_staff


class ListAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request, view):
        return view.action != 'list' or request.user and request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS or
                request.user and
                request.user.is_staff
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated to only owner of object or staff.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            try:
                if hasattr(obj, 'created_by') and obj.created_by == request.user:
                    return True
                elif obj == request.user:
                    return True
                elif request.user.is_staff:
                    return True
                else:
                    return False
            except:
                return False


class ReportHidePermission(permissions.BasePermission):
    """
    If logged in user is owner of object, user can not report its own object
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            try:
                if hasattr(obj, 'created_by') and obj.created_by == request.user:
                    return False
                else:
                    return True
            except:
                return False
