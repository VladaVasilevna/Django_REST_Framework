from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from .models import CourseSubscription, Course


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return "Course not found"

    subscribers = CourseSubscription.objects.filter(course=course).select_related('user')
    emails = [sub.user.email for sub in subscribers if sub.user.email]

    if not emails:
        return "No subscribers with email"

    subject = f"Обновление курса: {course.title}"
    message = (
        f"Здравствуйте!\n\n"
        f"Курс '{course.title}' был обновлен. "
        f"Пожалуйста, зайдите на платформу, чтобы ознакомиться с новыми материалами.\n\n"
        f"Спасибо, что вы с нами!"
    )
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, emails, fail_silently=False)
    return f"Sent emails to {len(emails)} subscribers"
