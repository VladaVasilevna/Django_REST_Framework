from django.urls import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        # Создание пользователей
        self.user = User.objects.create(email='user@sky.pro', password='0101')
        self.course = Course.objects.create(title='Test Course', description='Test description')
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test description',
                                            video_url='https://www.youtube.com/watch?v=video_id', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)


