from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserserializer,
)


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "email", "password", "first_name", "last_name"]


class UserSerializer(BaseUserserializer):
    class Meta(BaseUserserializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
