from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, IntervalSchedule

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    threshold_date = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Заблокировано {count} неактивных пользователей"


def setup_periodic_tasks():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Deactivate inactive users daily",
        task="users.tasks.deactivate_inactive_users",
        defaults={"enabled": True},
    )
