from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.core.models import BaseModel
from apps.users.queryset.user import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=1000, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        db_table = "users"


class Word(BaseModel):
    front = models.CharField(max_length=500, unique=True)
    back = models.CharField(max_length=500, unique=True)
    pronunciation = models.CharField(max_length=500, unique=True)
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="words")

    class Meta:
        db_table = "words"
