from rest_framework import serializers
from .models import CustomUser, Client, Contract, Event


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'password']
        extra_kwargs = {'id': {'read_only': True}}

    @staticmethod
    def create_user(email, password, role, first_name, last_name):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = CustomUser.objects.create(
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        if user.role == 'staff':
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'date_creation': {'read_only': True},
            'date_update': {'read_only': True},
            'sales': {'read_only': True},
        }


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'sales': {'read_only': True},
            'date_creation': {'read_only': True},
            'date_update': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'support': {'read_only': True},
            'date_creation': {'read_only': True},
            'date_update': {'read_only': True},
        }

