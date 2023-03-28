from django.db import models
from core.models import BaseEntity


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
    # Planet id in the star wars API
    sw_planet_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'planet'
