from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    preview_image = models.ImageField(
        upload_to="courses/", verbose_name="Загрузите изображение"
    )
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
