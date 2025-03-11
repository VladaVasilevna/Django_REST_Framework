from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserProfileSerializer


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
