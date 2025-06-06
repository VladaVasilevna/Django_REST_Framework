from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModer, IsOwner

from .models import Course, CourseSubscription, Lesson
from .paginators import LessonCoursePagination
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Course, позволяет выполнять CRUD-операции."""

    pagination_class = LessonCoursePagination
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

    def get_serializer_context(self):
        return {"request": self.request}


class LessonListCreate(generics.ListCreateAPIView):
    """Generic-класс для создания и просмотра уроков."""

    pagination_class = LessonCoursePagination
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


class CourseSubscriptionView(APIView):
    """Контроллер для управления подпиской на курс."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            course_id = int(request.data.get("course_id"))
            if not course_id:
                return Response(
                    {"error": "course_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            course = get_object_or_404(Course, pk=course_id)

            subs_item = CourseSubscription.objects.filter(user=user, course=course)

            if subs_item.exists():
                subs_item.delete()
                message = "Подписка удалена"
            else:
                CourseSubscription.objects.create(user=user, course=course)
                message = "Подписка добавлена"

            return Response({"message": message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
