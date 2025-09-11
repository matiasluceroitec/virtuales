from django.conf import settings
from rest_framework.permissions import BasePermission


VALID_TOKENS = [
    "token-valido-1234",
    "777777"
]

class TokenPermission(BasePermission):
    """
    Permiso basado en un header Authorization: Bearer <Token>
    """
    message = "Token no valido"

    def has_permission(self, request, view):
        print(request.user)
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if not auth_header.startswith("Bearer "):
            return False
        token = auth_header.split(" ", 1)[1].strip()
        return token in settings.VALID_TOKENS
            
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
            
