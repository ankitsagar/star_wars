from django.db import models
from core.models import BaseEntity
from planets.models import Planet
from movies.models import Movie


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


class UserMovie(CommonUserData):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class meta:
        db_table = 'user_movies'


class UserPlanet(CommonUserData):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    class meta:
        db_table = 'user_planets'
