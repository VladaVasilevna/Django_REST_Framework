from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwnerOrModer

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
                IsOwnerOrModer,
            ]  # Только модераторы могут создавать и удалять курсы
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            # Любой авторизованный пользователь может просматривать и редактировать курсы
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrModer]
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
        IsOwnerOrModer,
    ]  # Только модераторы могут создавать уроки

    def perform_create(self, serializer):
        """Привязывает урок к создавшему его пользователю."""
        serializer.save(owner=self.request.user)


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    """Generic-класс для просмотра, редактирования и удаления урока."""

    queryset = Lesson.objects.all()  # Получение всех уроков
    serializer_class = LessonSerializer
    # Только владельцы или модераторы могут редактировать/удалять уроки
    permission_classes = [IsAuthenticated, IsOwnerOrModer]

    def get_object(self):
        """Возвращает объект урока и проверяет права доступа."""
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
