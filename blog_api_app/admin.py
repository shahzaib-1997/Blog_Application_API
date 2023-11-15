from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    User,
    Post,
    Comment,
)

# Register your models here
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ["email", "username"]
    fieldsets = [
        (
            None,
            {
                "fields": ["email", "username", "password", "profile", "is_active", "is_staff", "is_superuser"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields" : ["last_login", "date_joined", "user_permissions"],
            },
        ),
    ]

admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(UserWhitelistToken)

# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


admin.site.site_header = "Blog Application API"
admin.site.index_title = "Admin Panel"
