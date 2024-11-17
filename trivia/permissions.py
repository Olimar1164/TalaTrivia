from rest_framework.permissions import BasePermission
from trivia.models import User  # Importar nuestro modelo User personalizado

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y tiene el rol correcto
        try:
            return bool(request.user and request.user.role == 'admin')
        except AttributeError:
            return False

class IsPlayerUser(BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.role == 'player')
        except AttributeError:
            return False