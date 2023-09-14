from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscribe, User


class MyUserSerializer(UserSerializer):
    """Сериализатор для модели User"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
            )

    def get_is_subscribed(self, obj):
        """ Проверка подписки. """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=user, author=obj.id).exists()


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля (set_password)"""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
