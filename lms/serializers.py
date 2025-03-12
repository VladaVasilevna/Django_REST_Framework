from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"  # Все поля модели Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lessons")

    class Meta:
        model = Course
        fields = "__all__"  # Все поля модели Course

    def get_lessons_count(self, obj):
        return obj.lessons.count()
