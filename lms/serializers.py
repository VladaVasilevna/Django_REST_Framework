from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson, включает все поля модели."""

    class Meta:
        model = Lesson
        fields = "__all__"  # Все поля модели Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course, включает все поля модели и дополнительные поля."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lessons")

    class Meta:
        model = Course
        fields = "__all__"  # Все поля модели Course

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()
