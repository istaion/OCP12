from rest_framework import serializers
from .models import CustomUser


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
        if not last_name:
            last_name = ''
        if not first_name:
            first_name = ''
        user = CustomUser.objects.create(
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        if user.role == 'staff':
            user.superuser = True
            user.save()
        return user

