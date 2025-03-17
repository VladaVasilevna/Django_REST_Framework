from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя, расширяет стандартную модель User."""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    REQUIRED_FIELDS = [
        "username"
    ]  # Поля, которые запрашиваются при создании суперпользователя
    USERNAME_FIELD = "email"  # Авторизация через email вместо username

    def __str__(self):
        """Возвращает email пользователя."""
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Хранит информацию о платеже, включая дату, сумму и метод оплаты."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    PAYMENT_METHODS = (
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, verbose_name="Способ оплаты"
    )

    def __str__(self):
        """Возвращает информацию о платеже."""
        return f"Платеж {self.user} на сумму {self.payment_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
