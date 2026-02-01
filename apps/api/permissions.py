from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Solo amministratori possono accedere."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.role == 'admin'
        )


class IsEditorOrAdmin(BasePermission):
    """Editor e amministratori."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.role in ('admin', 'editor')
        )


class IsOwnerOrAdmin(BasePermission):
    """A livello di oggetto: admin vede tutto, gli altri solo i propri."""
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == 'admin':
            return True
        return getattr(obj, 'owner_id', None) == request.user.id
