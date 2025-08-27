from django.contrib.auth.models import User
from rest_framework import serializers

from products.models import Customer


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
