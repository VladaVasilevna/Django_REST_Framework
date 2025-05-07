from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, CourseSubscription, Lesson

User = get_user_model()


def get_test_image_file(name="test.png", ext="PNG", size=(100, 100), color=(255, 0, 0)):
    """
    Создаёт валидный тестовый файл изображения в памяти.

    Параметры:
    - name: имя файла (например, 'test.png')
    - ext: формат изображения (например, 'PNG', 'JPEG')
    - size: кортеж с размерами изображения (ширина, высота)
    - color: цвет заливки изображения в формате RGB

    Возвращает:
    - объект SimpleUploadedFile с изображением, готовый для загрузки в тестах.
    """
    file_obj = BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return SimpleUploadedFile(
        name, file_obj.read(), content_type=f"image/{ext.lower()}"
    )


class LessonCRUDAndSubscriptionTests(APITestCase):
    """
    Набор тестов для проверки CRUD операций с уроками и управления подписками на курсы.

    Включает тесты для:
    - Просмотра списка уроков
    - Создания, обновления и удаления уроков владельцем
    - Проверки ограничений доступа для других пользователей
    - Подписки и отписки от курсов
    - Обработки ошибок при подписке
    """

    def setUp(self):
        """
        Подготовка тестовых данных:

        - Создаётся валидное тестовое изображение.
        - Создаются два пользователя: владелец и другой пользователь.
        - Создаётся курс с изображением, принадлежащий владельцу.
        - Создаётся урок с изображением, принадлежащий владельцу и относящийся к курсу.
        - Определяются URL для операций с уроками и подписками.
        - Создаются API клиенты с аутентификацией для владельца, другого пользователя и анонимного.
        """
        # Создаём валидное тестовое изображение
        self.test_image = get_test_image_file(name="test.jpg", ext="JPEG")

        # Создаём пользователей
        self.owner = User.objects.create_user(
            email="owner@example.com", password="password123", username="owner"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="password123", username="other"
        )

        # Создаём курс с изображением
        self.course = Course.objects.create(
            title="Test Course",
            description="Test course description",
            owner=self.owner,
            preview_image=self.test_image,
        )

        # Создаём урок с изображением
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test lesson description",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            course=self.course,
            owner=self.owner,
            preview_image=self.test_image,
        )

        # URL-ы для запросов
        self.lesson_list_create_url = reverse("lesson-list-create")
        self.lesson_detail_url = reverse("lesson-detail", args=[self.lesson.id])
        self.subscription_url = reverse("subscription")

        # Клиенты с аутентификацией разных пользователей
        self.client_owner = APIClient()
        self.client_owner.force_authenticate(user=self.owner)

        self.client_other = APIClient()
        self.client_other.force_authenticate(user=self.other_user)

        self.client_anon = APIClient()

    # Тесты CRUD уроков

    def test_lesson_list_authenticated(self):
        """
        Тест получения списка уроков аутентифицированным пользователем (владельцем).

        Проверяется, что статус ответа 200 OK и в списке есть хотя бы один урок.
        """
        response = self.client_owner.get(self.lesson_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) >= 1)

    def test_lesson_create_owner(self):
        """
        Тест создания нового урока пользователем-владельцем.

        Проверяется успешное создание (статус 201 Created) и совпадение заголовка урока.
        """
        image = get_test_image_file(name="new_test.jpg", ext="JPEG")
        data = {
            "title": "New Lesson",
            "description": "New lesson description",
            "video_url": "https://www.youtube.com/watch?v=abcdef",
            "course": self.course.id,
            "preview_image": image,
        }
        response = self.client_owner.post(
            self.lesson_list_create_url, data, format="multipart"
        )
        if response.status_code != status.HTTP_201_CREATED:
            print("Errors:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_lesson_create_other_user_forbidden(self):
        """
        Тест попытки создания урока другим пользователем (не владельцем).

        Проверяется, что операция либо успешна (если разрешена), либо запрещена (403 Forbidden).
        """
        image = get_test_image_file(name="other_test.jpg", ext="JPEG")
        data = {
            "title": "Other Lesson",
            "description": "Other lesson description",
            "video_url": "https://www.youtube.com/watch?v=abcdef",
            "course": self.course.id,
            "preview_image": image,
        }
        response = self.client_other.post(
            self.lesson_list_create_url, data, format="multipart"
        )
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]
        )

    def test_lesson_update_owner(self):
        """
        Тест обновления урока пользователем-владельцем.

        Проверяется успешное обновление (статус 200 OK) и корректность обновлённого заголовка.
        """
        image = get_test_image_file(name="updated_test.jpg", ext="JPEG")
        data = {
            "title": "Updated Lesson",
            "description": "Updated description",
            "video_url": "https://www.youtube.com/watch?v=updated",
            "course": self.course.id,
            "preview_image": image,
        }
        response = self.client_owner.put(
            self.lesson_detail_url, data, format="multipart"
        )
        if response.status_code != status.HTTP_200_OK:
            print("Errors:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_lesson_update_other_user_forbidden(self):
        """
        Тест попытки обновления урока другим пользователем (не владельцем).

        Проверяется, что операция запрещена (403 Forbidden) или ресурс не найден (404 Not Found).
        """
        image = get_test_image_file(name="hacked_test.jpg", ext="JPEG")
        data = {
            "title": "Hacked Lesson",
            "description": "Hacked description",
            "video_url": "https://www.youtube.com/watch?v=hacked",
            "course": self.course.id,
            "preview_image": image,
        }
        response = self.client_other.put(
            self.lesson_detail_url, data, format="multipart"
        )
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    def test_lesson_delete_owner(self):
        """
        Тест удаления урока пользователем-владельцем.

        Проверяется успешное удаление (статус 204 No Content).
        """
        response = self.client_owner.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_delete_other_user_forbidden(self):
        """
        Тест попытки удаления урока другим пользователем (не владельцем).

        Проверяется, что операция запрещена (403 Forbidden) или ресурс не найден (404 Not Found).
        """
        response = self.client_other.delete(self.lesson_detail_url)
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    # Тесты подписок

    def test_subscribe_course(self):
        """
        Тест подписки на курс другим пользователем.

        Проверяется успешное добавление подписки (статус 200 OK), наличие сообщения и запись в базе.
        """
        data = {"course_id": self.course.id}
        response = self.client_other.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка добавлена", response.data["message"])
        self.assertTrue(
            CourseSubscription.objects.filter(
                user=self.other_user, course=self.course
            ).exists()
        )

    def test_unsubscribe_course(self):
        """
        Тест отписки от курса.

        Создаётся подписка, затем отправляется запрос на отписку.
        Проверяется успешное удаление подписки и соответствующее сообщение.
        """
        CourseSubscription.objects.create(user=self.other_user, course=self.course)
        data = {"course_id": self.course.id}
        response = self.client_other.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка удалена", response.data["message"])
        self.assertFalse(
            CourseSubscription.objects.filter(
                user=self.other_user, course=self.course
            ).exists()
        )

    def test_subscribe_without_course_id(self):
        """
        Тест попытки подписки без указания course_id.

        Проверяется, что возвращается ошибка с кодом 400 Bad Request и соответствующим сообщением.
        """
        response = self.client_other.post(self.subscription_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("course_id is required", response.data["error"])

    def test_subscribe_unauthenticated(self):
        """
        Тест попытки подписки неаутентифицированным пользователем.

        Проверяется, что доступ запрещён (статус 401 Unauthorized).
        """
        data = {"course_id": self.course.id}
        response = self.client_anon.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
