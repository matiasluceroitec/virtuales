from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from api.serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
    """
    GET /api/users
        return -> [UserSerializer]
    POST /api/users/ -> Crea usuario
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/users/<pk>
        return -> UserSerializer
    PUT /api/users/<pk> -> Actualiza totalmente
    PATCH /api/users/<pk> -> Actualizacion Parcial
    DETELE /api/users/<pk> -> Elimina
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
