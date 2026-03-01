from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # This inherits is_staff, is_superuser, and is_active automatically
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username