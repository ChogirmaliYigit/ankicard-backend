from django.contrib import admin
from unfold.admin import ModelAdmin
from users.models import CustomToken, User, Word


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "username",
        "full_name",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    fields = (
        "full_name",
        "username",
        "is_active",
        "is_staff",
    )
    search_fields = (
        "full_name",
        "username",
        "id",
    )

    list_filter_submit = True


@admin.register(Word)
class WordAdmin(ModelAdmin):
    list_display = (
        "front",
        "back",
        "pronunciation",
        "user",
        "is_favorite",
    )
    fields = list_display
    search_fields = list_display + ("id",)
    list_filter = ("is_favorite",)
    list_filter_submit = True


@admin.register(CustomToken)
class CustomTokenAdmin(ModelAdmin):
    list_display = (
        "key",
        "user",
        "created",
        "expires_at",
    )
    fields = (
        "key",
        "user",
        "expires_at",
    )
    search_fields = list_display
