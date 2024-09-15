
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Customer(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name
