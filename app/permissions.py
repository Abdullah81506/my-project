from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS — allowed for any authenticated user
        if request.method in SAFE_METHODS:
            return True
        # For PUT, PATCH, DELETE — only the author can proceed
        return obj.author == request.user
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user