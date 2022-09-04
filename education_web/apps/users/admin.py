from django.contrib import admin
from apps.users.models import UserProfile
from django.contrib.auth.admin import UserAdmin
class UserProfileAmdin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserAdmin)