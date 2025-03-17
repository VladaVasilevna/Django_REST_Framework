from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Payment, включает все поля модели."""

    class Meta:
        model = Payment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя, включает все поля модели."""

    payment_history = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "avatar",
            "payment_history",
        ]


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для общедоступной информации профиля пользователя."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "phone",
            "city",
            "avatar",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        """Проверяет корректность данных при регистрации."""
        email = attrs.get("email", "")
        if not len(email):
            raise serializers.ValidationError(
                {"email": "Электронная почта обязательна"}
            )
        return attrs

    def create(self, validated_data):
        """Создаёт нового пользователя."""
        return User.objects.create_user(**validated_data)
