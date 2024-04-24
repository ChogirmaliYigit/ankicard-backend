from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.users.queryset.user import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=1000, null=True, blank=True)
    last_name = models.CharField(max_length=1000, null=True, blank=True)
    username = models.CharField(max_length=1000, unique=True)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    @property
    def full_name(self):
        first_name = str(self.first_name) if self.first_name else ""
        last_name = str(self.last_name) if self.last_name else ""
        full_name = " ".join([first_name, last_name])
        return full_name.strip()

    class Meta:
        db_table = "users"
