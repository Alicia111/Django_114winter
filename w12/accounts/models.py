from django.contrib.auth.models import AbstractUser
from django.db import models


# Standalone Ch10: define CustomUser here instead of inheriting from Ch9.
# `age` is displayed on the homepage in Stage 2.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
