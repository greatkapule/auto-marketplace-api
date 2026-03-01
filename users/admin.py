from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# This ensures the Django Admin uses the correct forms for your Custom User
admin.site.register(User, UserAdmin)