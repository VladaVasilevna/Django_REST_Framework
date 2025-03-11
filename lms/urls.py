from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonDetail, LessonListCreate

router = DefaultRouter()
router.register(r"courses", CourseViewSet)  # Регистрация ViewSet для курса

urlpatterns = [
    path("", include(router.urls)),  # Включение маршрутов из роутера
    path(
        "lessons/", LessonListCreate.as_view(), name="lesson-list-create"
    ),  # Список и создание уроков
    path(
        "lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"
    ),  # Получение, изменение и удаление урока
]
