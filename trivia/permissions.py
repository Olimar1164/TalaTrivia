from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'role'):
            print('User is not authenticated or does not have a role attribute')
            return False
        is_admin = request.user.role == 'admin'
        print(f"User: {request.user.username}, Role: {request.user.role}, Is Admin: {is_admin}")
        return is_admin
class IsPlayerUser(BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.role == 'player')
        except AttributeError:
            return False