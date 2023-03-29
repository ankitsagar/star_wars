# DRF
from rest_framework import serializers

# App
from users.models import User


class BaseUserMetadataSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()

    def get_user_metdata_obj(self, obj):
        if getattr(obj, self.user_metadata_attr):
            return getattr(obj, self.user_metadata_attr)[0]
        return None

    def get_is_favorite(self, obj):
        user_metadata = self.get_user_metdata_obj(obj)
        if user_metadata:
            return user_metadata.is_favorite
        else:
            return False

    def get_created_time(self, obj):
        user_metadata = self.get_user_metdata_obj(obj)
        if user_metadata:
            return user_metadata.created_time
        else:
            return obj.created_time

    def get_updated_time(self, obj):
        user_metadata = self.get_user_metdata_obj(obj)
        if user_metadata:
            return user_metadata.updated_time
        else:
            return obj.updated_time


class BaseUserMetadataCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_favorite = serializers.BooleanField()
    custom_name = serializers.CharField(
        min_length=1, max_length=100, required=False)

    def create(self, validated_data):
        model_instance = self.context[self.model_context_key]
        model_service = self.model_service()
        user_metadata = model_service.create_or_update_user_metadata_entry(
            model_instance, **validated_data)
        return user_metadata
