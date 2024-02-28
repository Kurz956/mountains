from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from appusers.models import User

admin.site.register(User, UserAdmin)
