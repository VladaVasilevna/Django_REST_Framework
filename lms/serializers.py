from rest_framework import serializers

from .models import Course, Lesson, CourseSubscription
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson, включает все поля модели."""

    video_url = serializers.URLField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"  # Все поля модели Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course, включает все поля модели и дополнительные поля."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lessons")
    is_subscribed = serializers.SerializerMethodField()


    class Meta:
        model = Course
        fields = "__all__"  # Все поля модели Course

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return CourseSubscription.objects.filter(user=request.user, course=obj).exists()
        return False
