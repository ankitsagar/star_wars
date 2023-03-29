# Django
from django.db import models

# App
from core.models import BaseEntity


class User(BaseEntity):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)

    class Meta:
        db_table = 'user'


class CommonUserData(BaseEntity):
    """ Common user fields which exists between user and other entities"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        abstract = True
