# DRF
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

# App
from movies import constants
from movies.serializers import MovieSerializer, UserMovieCreateSerializer
from movies.services import MovieService
from users.services import UserService


class GetMovies(ListAPIView):
    serializer_class = MovieSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.movie_service = MovieService()

    def list(self, request, user_id, *args, **kwargs):
        query = request.query_params.get('query')
        # Validate given user id is correct
        user = self.user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise NotFound(detail="user id not found")
        movie_queryset = self.movie_service.get_movies_with_user_movies(
            user=user, query=query)
        page = self.paginate_queryset(movie_queryset)
        serializer = self.serializer_class(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return response


class CreateUserMovie(UpdateAPIView):
    serializer_class = UserMovieCreateSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_service = MovieService()

    def put(self, request, movie_id, *args, **kwargs):
        movie = self.movie_service.get_movie_by_id(movie_id=movie_id)
        if not movie:
            raise NotFound(detail="movie id not found")

        serializer = self.serializer_class(
            data=request.data, context={constants.MOVIE: movie}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
