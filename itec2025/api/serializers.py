from django.contrib.auth.models import User
from rest_framework import serializers

from products.models import Customer, Category, Product


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
    )

    class Meta:
        model = User
        fields = [
            'pk','username','email','first_name',
            'last_name','is_active','password'
        ]
        
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password(User.objects.make_random_password())
            # Enviarle la contraseña por email
        user.save()
        Customer.objects.create(
            name=user.first_name,
            email=user.email,
            phone=1234
        )
        return user


    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        # Opcion 1
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

        # Opcion 2
        #instance = User.objects.create(
        #    username=validated_data['username'],
        #    email=validated_data['email'],
        #    first_name=validated_data['first_name'],
        #    last_name=validated_data['last_name'],
        #)
        #instance.set_password(password)
        #instance.save()
        #return instance


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
class CategoryForProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    category = CategoryForProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.price * obj.stock
    
    def get_image(self, obj):
        if not obj.image:
            return "No contiene imagen"
        return obj.image.url


