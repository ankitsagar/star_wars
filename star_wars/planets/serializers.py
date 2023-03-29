# DRF
from rest_framework import serializers

# App
from common.serializers import (
    BaseUserMetadataSerializer,
    BaseUserMetadataCreateSerializer
)
from planets import constants
from planets.models import Planet
from planets.services import PlanetService


class PlanetSerializer(BaseUserMetadataSerializer):
    user_metadata_attr = constants.USER_PLANET_ATTR
    name = serializers.SerializerMethodField()

    class Meta:
        model = Planet
        fields = '__all__'

    def get_name(self, obj):
        user_metadata = self.get_user_metdata_obj(obj)
        if user_metadata:
            return user_metadata.custom_name
        else:
            return obj.name


class UserPlanetCreateSerializer(BaseUserMetadataCreateSerializer):
    model_context_key = constants.PLANET
    model_service = PlanetService
