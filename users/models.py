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
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплатить курс",
        help_text="Укажите курс для оплаты",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )

    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
    )

    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )
    PAYMENT_METHODS = (
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("stripe", "Stripe"),
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        verbose_name="Способ оплаты",
        help_text="Укажите способ оплаты",
        default="stripe",
    )

    def __str__(self):
        """Возвращает информацию о платеже."""
        return f"Платеж {self.user} на сумму {self.amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
