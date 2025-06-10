from django.apps import AppConfig
import sys


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Вызываем setup_periodic_tasks только если команда runserver или celery
        if 'runserver' in sys.argv or 'celery' in sys.argv:
            from users.tasks import setup_periodic_tasks
            setup_periodic_tasks()

