# Django
from django.db import models
from django.contrib.postgres.fields import ArrayField

# App
from core.models import BaseEntity
from planets import constants
from users.models import CommonUserData


class Planet(BaseEntity):
    name = models.CharField(max_length=100)
    rotation_period = models.CharField(max_length=40)
    orbital_period = models.CharField(max_length=40)
    diameter = models.CharField(max_length=40)
    climate = models.CharField(max_length=40)
    gravity = models.CharField(max_length=40)
    terrain = models.CharField(max_length=40)
    surface_water = models.CharField(max_length=40)
    population = models.CharField(max_length=40)
    films = ArrayField(models.CharField(max_length=500), null=True)
    url = models.CharField(max_length=500)

    class Meta:
        db_table = 'planet'
        ordering = ('name',)


class UserPlanet(CommonUserData):
    planet = models.ForeignKey(
        Planet,
        on_delete=models.CASCADE,
        related_name=constants.PLANET_TO_USER_REL)

    class meta:
        db_table = 'user_planets'
        ordering = ('custom_name',)
        unique_together = (('user_id', 'planet_id'), )
