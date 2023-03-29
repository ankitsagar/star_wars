# App
from movies.models import Movie


class MovieService:

    def bulk_create(self, movies_data):
        objs = []
        fields = [field.name for field in Movie._meta.get_fields()]
        for movie_data in movies_data:
            for key in list(movie_data.keys()):
                if key not in fields:
                    movie_data.pop(key)
            objs.append(Movie(**movie_data))
        Movie.objects.bulk_create(objs=objs)
