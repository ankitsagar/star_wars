# Django
from django.db import models

# App
from core.models import BaseEntity
from users.models import CommonUserData


class Movie(BaseEntity):
    title = models.CharField(max_length=100)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField(max_length=1000)
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    release_date = models.DateField()
    # Film id in the star wars API
    url = models.CharField(max_length=500)

    class Meta:
        db_table = 'movie'
        ordering = ('title', )


class UserMovie(CommonUserData):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="user_movies")

    class meta:
        db_table = 'user_movies'
        ordering = ('custom_name',)
        unique_together = (('user_id', 'movie_id'), )
