from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only grant owners of an object write access.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user
    
    
class IsSelfOrReadOnly(permissions.BasePermission):
        """
        Custom permission to allow users write permissions to thier own profile
        """
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj == request.user