from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Course, позволяет выполнять CRUD-операции."""

    queryset = Course.objects.all()  # Получение всех курсов
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Определяет права доступа для каждого действия."""
        if self.action in ["create", "destroy"]:
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]  # Только владельцы могут создавать и удалять курсы
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            # Владелец или модератор могут просматривать и редактировать курсы
            permission_classes = [IsAuthenticated, IsOwner | IsModer]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Привязывает курс к создавшему его пользователю."""
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    """Generic-класс для создания и просмотра уроков."""

    queryset = Lesson.objects.all()  # Получение всех уроков
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]  # Только владелец может создавать уроки

    def perform_create(self, serializer):
        """Привязывает урок к создавшему его пользователю."""
        serializer.save(owner=self.request.user)


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    """Generic-класс для просмотра, редактирования и удаления урока."""

    queryset = Lesson.objects.all()  # Получение всех уроков
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Динамически определяем права для каждого действия"""
        if self.request.method in ["PUT", "PATCH", "GET"]:  # Редактирование и просмотр
            permission_classes = [IsAuthenticated, IsOwner | IsModer]
        elif self.request.method == "DELETE":  # Удаление
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
