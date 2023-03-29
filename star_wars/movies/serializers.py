# DRF
from rest_framework import serializers

# App
from movies import constants
from movies.models import Movie
from movies.services import UserMovieService
from users.models import User


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def __get_user_movie_obj(self, obj):
        if obj.user_movie:
            return obj.user_movie[0]
        return None

    def get_title(self, obj):
        user_movie = self.__get_user_movie_obj(obj)
        if user_movie and user_movie.custom_name:
            return user_movie.custom_name
        else:
            return obj.title

    def get_is_favorite(self, obj):
        user_movie = self.__get_user_movie_obj(obj)
        if user_movie:
            return user_movie.is_favorite
        else:
            return False

    def get_created_time(self, obj):
        user_movie = self.__get_user_movie_obj(obj)
        if user_movie:
            return user_movie.created_time
        else:
            return obj.created_time

    def get_updated_time(self, obj):
        user_movie = self.__get_user_movie_obj(obj)
        if user_movie:
            return user_movie.updated_time
        else:
            return obj.updated_time


class UserMovieCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_favorite = serializers.BooleanField()
    custom_name = serializers.CharField(
        min_length=1, max_length=100, required=False)

    def create(self, validated_data):
        movie = self.context[constants.MOVIE]
        user_movie_service = UserMovieService()
        user_movie = user_movie_service.create_or_update_user_movie(
            movie=movie, **validated_data)
        return user_movie
