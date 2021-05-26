from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCurrentUserOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if bool(request.user.is_superuser):
            return True
        
        if hasattr(obj, 'user'):
            return bool(request.user == obj.user)
        elif hasattr(obj, 'exit'):
            return bool(request.user == obj.exit.user)
        elif hasattr(obj, 'entry'):
            return bool(request.user == obj.entry.user)
        else:
            return False

class IsSuperUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_superuser or
            request.method in SAFE_METHODS
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_superuser or
            request.method in SAFE_METHODS
        )

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_superuser
        )
        

