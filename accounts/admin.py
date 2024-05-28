from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["username", "role"]
    list_filter = ("role",)
    search_fields = (
        "first_name",
        "last_name",
        "username",
    )
    fieldsets = (
        (None, {"fields": ("username", "password", "role")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "role"),
            },
        ),
    )


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "image_tag"]

    def image_tag(self, obj):
        return format_html('<img src="{}" width="80px" />'.format(obj.image))

    image_tag.short_description = "Avatar"
    image_tag.allow_tags = True
