from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    email=models.EmailField(unique=True, db_index=True)
    timezone=models.CharField(max_length=64, default='UTC')
    USERNAME_FIELD='email'; REQUIRED_FIELDS=['username']
    class Meta: indexes=[models.Index(fields=['email','is_active'])]
    def __str__(self): return self.email
