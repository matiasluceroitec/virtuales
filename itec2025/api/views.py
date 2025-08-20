from django.contrib.auth.models import User
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response

from api.serializers import (
    CustomerSerializer,
    UserSerializer, 
)
from products.models import Customer


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

    def perform_destroy(self, instance):
        if instance.is_active:
            instance.is_active = False
            instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance=instance)
        return Response(
            {
                "detail":f'User {instance.username} deactivated'
            }, 
            status=status.HTTP_200_OK
        )   
    

class CustomerListCreateView(ListCreateAPIView):
    """
    GET /api/customer
        return -> [CustomerSerializer]
    POST /api/customer/ -> Crea customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer