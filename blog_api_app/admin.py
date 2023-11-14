from django.contrib import admin
from .models import (
    User,
    Post,
    Comment,
    UserWhitelistToken
)

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserWhitelistToken)


admin.site.site_header = "Blog Application API"
admin.site.index_title = ""
admin.site.site_title = "Admin Panel"