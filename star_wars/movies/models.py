from django.db import models
from core.models import BaseEntity

# Create your models here.


class Movie(BaseEntity):
    title = models.CharField(max_length=100)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField(max_length=1000)
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    release_date = models.DateField()
    # Film id in the star wars API
    sw_movie_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'movie'
