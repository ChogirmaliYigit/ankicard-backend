from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

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
    front = models.CharField(max_length=500)
    back = models.CharField(max_length=500)
    pronunciation = models.CharField(max_length=500)
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="words")

    class Meta:
        db_table = "words"
        unique_together = ("front", "back", "pronunciation", "user")


def get_default_time():
    return timezone.now() + timedelta(days=settings.DEFAULT_TOKEN_EXPIRE_DAYS)


class CustomToken(Token):
    expires_at = models.DateTimeField(
        default=get_default_time,
        editable=False,
    )

    class Meta:
        db_table = "custom_tokens"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        CustomToken.objects.update_or_create(
            defaults={
                "user": instance,
            },
            expires_at=timezone.now()
            + timedelta(days=settings.DEFAULT_TOKEN_EXPIRE_DAYS),
        )
