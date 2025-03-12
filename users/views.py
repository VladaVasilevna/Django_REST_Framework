from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Только аутентифицированные пользователи могут редактировать свой профиль

    def get_object(self):
        return (
            self.request.user
        )  # Возвращаем текущего аутентифицированного пользователя


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
