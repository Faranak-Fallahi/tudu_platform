from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.managers import CustomUserManager
from config import settings


class User(AbstractUser):
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    def __str__(self):
        return self.user.username
    