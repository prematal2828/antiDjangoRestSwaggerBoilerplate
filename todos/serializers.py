"""
Serializers for the todos app.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Full Todo serializer (list + detail)."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Todo
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "priority",
            "is_completed",
            "due_date",
            "image",
            "image_url",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "image_url", "created_at", "updated_at")
        extra_kwargs = {
            "image": {"write_only": True, "required": False},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class TodoUpdateSerializer(serializers.ModelSerializer):
    """Serializer used for PUT/PATCH — owner is immutable."""

    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Todo
        fields = ("title", "description", "priority", "is_completed", "due_date", "image", "image_url")
        extra_kwargs = {
            "image": {"write_only": True, "required": False},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
