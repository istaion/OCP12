from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

roles_list = [
    ('sales', 'sales'),
    ('support', 'support'),
    ('staff', 'staff')
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


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField("email address")
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    existing = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    sales = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)


class Contract(models.Model):
    amount = models.IntegerField()
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    payment_due = models.DateTimeField(null=True)
    signed = models.BooleanField(default=False)


class Event(models.Model):
    title = models.CharField(max_length=50, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    support = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True)

