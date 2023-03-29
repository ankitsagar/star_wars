# DRF
from rest_framework import serializers

# App
from common.serializers import (
    BaseUserMetadataSerializer,
    BaseUserMetadataCreateSerializer
)
from movies import constants
from movies.models import Movie
from movies.services import MovieService


class MovieSerializer(BaseUserMetadataSerializer):
    user_metadata_attr = constants.USER_MOVIE_ATTR
    title = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_title(self, obj):
        user_metadata = self.get_user_metdata_obj(obj)
        if user_metadata:
            return user_metadata.custom_name
        else:
            return obj.title


class UserMovieCreateSerializer(BaseUserMetadataCreateSerializer):
    model_context_key = constants.MOVIE
    model_service = MovieService
