from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerManager(BaseUserManager):
    """ Handles creation of regular users and superusers with email as the unique identifier instead of username. """

    def create_user(self, email, name, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, password=None):
        user = self.create_user(email, name, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class CustomToken(models.Model):
    """ Model for storing custom authentication tokens."""
    
    key = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='custom_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Custom Token"
        verbose_name_plural = "Custom Tokens"