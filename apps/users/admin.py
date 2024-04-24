from django.contrib import admin
from unfold.admin import ModelAdmin
from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "is_active",
        "is_staff",
    )
    search_fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "id",
    )

    list_filter_submit = True
