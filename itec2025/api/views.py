from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.pagination import(
    PageNumberPagination, LimitOffsetPagination
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import (
    extend_schema_view, 
    extend_schema,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

from api.mixins import AuthAdminView, AuthView
from api.permissions import TokenPermission
from api.serializers import (
    CategorySerializer,
    CustomerSerializer,
    ProductSerializer,
    UserSerializer, 
)
from products.models import Category, Customer, Product



@extend_schema_view(
    get=extend_schema(
        summary="Listar Usuarios",
        description="Devuelve una lista de usuarios paginada",
        tags=["Usuarios"],
        responses={
            200: OpenApiResponse(
                response=UserSerializer(many=True)
            )
        }
    ),
    post=extend_schema(
        summary="Crea Usuario",
        description="Crea un usuario",
        tags=["Usuarios"],
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSerializer
            )
        }
    )
)
class UserListCreateView(ListCreateAPIView):
    """
    GET /api/users
        return -> [UserSerializer]
    POST /api/users/ -> Crea usuario
    """
    permission_classes = [IsAuthenticated] #TODOS LOS USUARIOS AUTENTICADOS PUEDEN VERLO
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema_view(
    delete=extend_schema(
        summary="Elimina Usuario",
        description="Elimina un usuario",
        tags=["Usuarios"],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT
            )
        }
    )
)
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/users/<pk>
        return -> UserSerializer
    PUT /api/users/<pk> -> Actualiza totalmente
    PATCH /api/users/<pk> -> Actualizacion Parcial
    DETELE /api/users/<pk> -> Elimina
    """
    permission_classes = [IsAuthenticated] #SOLO USUSARIOS ADMIN PUEDEN ACCEDER (BASIC AUTH)
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
    

class CustomerListCreateView(ListCreateAPIView, AuthView):
    """
    GET /api/customer
        return -> [CustomerSerializer]
    POST /api/customer/ -> Crea customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CategoryListCreateAPIView(APIView, AuthView):
    def get(self, request):
        qs = Category.objects.all().order_by('id')
        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                CategorySerializer(instance).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView, AuthAdminView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)
    
    def get(self, request, pk):
        instance = self.get_object(pk)
        return Response(
                CategorySerializer(instance).data,
            )

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                    CategorySerializer(instance).data
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(
                    CategorySerializer(instance).data
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductListCreateApiView(APIView):
    permission_classes = [TokenPermission]
    def get(self, request):
        qs = Product.objects.all()
        print(qs)
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)
    

class CustomerViewSet(viewsets.ModelViewSet, AuthView):
    """
    GENERA COMPLETAMENTE EL CRUD 
    Y GENERA LAS RUTAS
        - GET /api/customers-vs/
        - POST /api/customers-vs/
        - GET /api/customers-vs/{pk}
        - PUT /api/customers-vs/{pk}
        - PATCH /api/customers-vs/{pk}
        - DELETE /api/customers-vs/{pk}
    """

    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet, AuthView):
    """
    GENERA COMPLETAMENTE EL CRUD 
    Y GENERA LAS RUTAS
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
