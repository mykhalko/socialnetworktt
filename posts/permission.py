from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class LikeActions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.auth or not request.user:
            return False
        return request.method == 'POST'


class IsPostOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.auth or not request.user:
            return False
        return obj.author == request.user or request.user.is_staff
