from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_join = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email if self.email else self.phone_number


class RefreshTokenModels(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return self.user.username
