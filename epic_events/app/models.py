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
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Client(models.Model):
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField("email address", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=200)
    existing = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    sales = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True,
                              limit_choices_to={"role": "sales"})


class Contract(models.Model):
    amount = models.IntegerField(null=True, blank=True)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True,
                              limit_choices_to={"role": "sales"})
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    payment_due = models.DateTimeField(null=True, blank=True)
    signed = models.BooleanField(default=False)


class Event(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    attendees = models.IntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    event_date = models.DateTimeField(null=True, blank=True)
    support = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL,
                                null=True, limit_choices_to={"role": "support"})
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.client = self.contract.client
        event = super(Event, self)
        event.save()

        return event

