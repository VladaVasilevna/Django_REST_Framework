from django.conf import settings
from django.db import models


class Course(models.Model):
    """Хранит информацию о курсе, включая название, описание и изображение."""

    title = models.CharField(max_length=200, verbose_name="Название курса")
    preview_image = models.ImageField(
        upload_to="courses/", verbose_name="Загрузите изображение"
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        """Возвращает название курса."""
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Хранит информацию об уроке, включая название, описание и ссылку на видео."""

    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    preview_image = models.ImageField(
        upload_to="lessons/", verbose_name="Загрузите изображение"
    )
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name="Выберите курс",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        """Возвращает название урока."""
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class CourseSubscription(models.Model):
    """Модель подписки на курс."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        """Возвращает информацию о подписке."""
        return f"{self.user.username} на курс {self.course.title}"

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"
        unique_together = (
            "user",
            "course",
        )  # Уникальность подписки для пользователя и курса
