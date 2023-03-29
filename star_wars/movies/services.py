# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, Q

# App
from movies.models import Movie, UserMovie


class MovieService:

    def __init__(self):
        self.user_movie_service = UserMovieService()

    def get_movie_by_id(self, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except ObjectDoesNotExist:
            movie = None
        return movie

    def get_all_movies(self):
        return Movie.objects.all()

    def bulk_create(self, movies_data):
        objs = []
        fields = [field.name for field in Movie._meta.get_fields()]
        for movie_data in movies_data:
            for key in list(movie_data.keys()):
                if key not in fields:
                    movie_data.pop(key)
            objs.append(Movie(**movie_data))
        Movie.objects.bulk_create(objs=objs)

    def get_movies_with_user_movies(self, user, query=None):
        """
        Fetches all the movies with user movies table if there are user
        movie entry.
        """
        filter_args = []
        if query:
            user_movie_queryset = self.user_movie_service.get_user_movies(
                user_id=user.id, query=query
            )
            # These are the found movie ids which need to be included in the
            # result
            found_movie_ids = [
                user_movie.movie_id
                for user_movie in user_movie_queryset
            ]

            # We need all user's movies to avoid searching in movie table
            user_movie_ids = self.user_movie_service.get_movies_ids_from_user_movie(  # noqa
                user.id)

            # We need to apply a filter on movie table when the title contains
            # the query then it must not be the part of user movie table and
            # inculde all the search results from user movie table
            filter_args.append(
                (Q(title__icontains=query) & ~Q(id__in=user_movie_ids))
                | Q(id__in=found_movie_ids)
            )
        else:
            user_movie_queryset = self.user_movie_service.get_user_movies(
                user_id=user.id
            )

        movies = Movie.objects.prefetch_related(
            Prefetch(
                'user_movies',
                to_attr='user_movie',
                queryset=user_movie_queryset
            )
        ).filter(*filter_args)
        return movies


class UserMovieService:

    def get_user_movie(self, user_id, movie_id):
        try:
            user_movie = UserMovie.objects.get(
                user_id=user_id, movie_id=movie_id)
        except ObjectDoesNotExist:
            user_movie = None
        return user_movie

    def get_user_movies(self, user_id, query=None):
        """ Return all the movies related to the user """
        queryset = UserMovie.objects.filter(user_id=user_id)
        if query:
            queryset = queryset.filter(custom_name__icontains=query)
        return queryset

    def create_or_update_user_movie(
            self, movie, user, is_favorite, custom_name=None):
        user_movie = self.get_user_movie(user.id, movie.id)
        if not user_movie:
            user_movie = UserMovie(user=user, movie=movie)
        user_movie.is_favorite = is_favorite
        # If custom name is none then attach the orignal title
        user_movie.custom_name = custom_name or movie.title
        user_movie.save()
        return user_movie

    def get_movies_ids_from_user_movie(self, user_id):
        return self.get_user_movies(user_id).values_list(
            "movie_id", flat=True)
