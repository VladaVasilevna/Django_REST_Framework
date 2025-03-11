from rest_framework import generics, viewsets

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # Получение всех курсов
    serializer_class = CourseSerializer


# Generic-класс для модели Lesson
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()  # Получение всех уроков
    serializer_class = LessonSerializer


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()  # Получение всех уроков
    serializer_class = LessonSerializer
