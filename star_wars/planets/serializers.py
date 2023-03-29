# DRF
from rest_framework import serializers

# App
from planets import constants
from planets.models import Planet
from planets.services import UserPlanetService
from users.models import User


class PlanetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()

    class Meta:
        model = Planet
        fields = '__all__'

    def __get_user_planet_obj(self, obj):
        if obj.user_planet:
            return obj.user_planet[0]
        return None

    def get_name(self, obj):
        user_planet = self.__get_user_planet_obj(obj)
        if user_planet and user_planet.custom_name:
            return user_planet.custom_name
        else:
            return obj.name

    def get_is_favorite(self, obj):
        user_planet = self.__get_user_planet_obj(obj)
        if user_planet:
            return user_planet.is_favorite
        else:
            return False

    def get_created_time(self, obj):
        user_planet = self.__get_user_planet_obj(obj)
        if user_planet:
            return user_planet.created_time
        else:
            return obj.created_time

    def get_updated_time(self, obj):
        user_planet = self.__get_user_planet_obj(obj)
        if user_planet:
            return user_planet.updated_time
        else:
            return obj.updated_time


class UserPlanetCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_favorite = serializers.BooleanField()
    custom_name = serializers.CharField(
        min_length=1, max_length=100, required=False)

    def create(self, validated_data):
        planet = self.context[constants.PLANET]
        user_planet_service = UserPlanetService()
        user_planet = user_planet_service.create_or_update_user_planet(
            planet=planet, **validated_data)
        return user_planet
