from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.permissions import IsOwner

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import (PaymentSerializer, PublicUserProfileSerializer,
                          RegisterSerializer, UserProfileSerializer)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """Контроллер для редактирования профиля пользователя."""

    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]  # Только владелец может редактировать свой профиль

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от метода запроса."""
        if self.request.method == "GET":
            return PublicUserProfileSerializer  # Для просмотра общедоступной информации
        else:
            return UserProfileSerializer  # Для редактирования своего профиля

    def get_object(self):
        """Возвращает профиль текущего пользователя."""
        return self.request.user


class PublicUserProfileDetailView(generics.RetrieveAPIView):
    """Контроллер для просмотра общедоступной информации профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = PublicUserProfileSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Любой авторизованный пользователь может просматривать профиль


class PaymentListView(generics.ListAPIView):
    """Контроллер для просмотра списка платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]


class RegisterView(APIView):
    """Контроллер для регистрации пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токенов JWT."""

    def validate(self, attrs):
        """Добавляет username в ответ при получении токенов."""
        data = super().validate(attrs)
        data["username"] = self.user.username
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """Контроллер для получения токенов JWT."""

    serializer_class = MyTokenObtainPairSerializer


class UserListCreateView(generics.ListCreateAPIView):
    """Контроллер для создания и просмотра списка пользователей."""

    queryset = User.objects.all()
    serializer_class = PublicUserProfileSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Любой авторизованный пользователь может просматривать список


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Контроллер для просмотра, редактирования и удаления профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # Только владелец может редактировать или удалять свой профиль
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        """Возвращает объект профиля и проверяет права доступа."""
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
