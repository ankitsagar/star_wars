# App
from common.views import BaseUserMetaDataListView, BaseUserMetaDataCreateView
from movies import constants
from movies.serializers import MovieSerializer, UserMovieCreateSerializer
from movies.services import MovieService


class GetMovies(BaseUserMetaDataListView):
    serializer_class = MovieSerializer
    model_service_class = MovieService


class CreateUserMovie(BaseUserMetaDataCreateView):
    serializer_class = UserMovieCreateSerializer
    model_service_class = MovieService
    not_found_error = "movie id not found"
    instance_context_key = constants.MOVIE
