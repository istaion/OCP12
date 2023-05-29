from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

roles_list = [
    ('Sales', 'Sales'),
    ('Support', 'Support'),
    ('Staff', 'Staff')
]


class CustomUser(AbstractUser):
    username = None
    role = models.CharField(max_length=25, choices=roles_list, null=False)
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
