from rest_framework.permissions import IsAuthenticated, IsAdminUser

class AuthView:
    """
    Clase base para las vistas que requiqere autenticacion
    """
    permission_classes = [IsAuthenticated]

class AuthAdminView:
    """
    Clase base para las vistas que requiqere autenticacion de un usuario Admin
    """
    permission_classes = [IsAdminUser]

