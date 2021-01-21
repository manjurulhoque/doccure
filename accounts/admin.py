from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User, Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'role']
    list_filter = ("role",)
    search_fields = ("first_name", "last_name", "username",)


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "image_tag"]

    def image_tag(self, obj):
        return format_html('<img src="{}" width="80px" />'.format(obj.image))

    image_tag.short_description = 'Avatar'
    image_tag.allow_tags = True
