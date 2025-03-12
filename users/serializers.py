from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
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
