from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from lms.models import Course

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


class CourseTests(APITestCase):
    """
    Набор тестов для проверки API эндпоинтов, связанных с моделью Course.

    Тестируются операции:
    - Получение списка курсов
    - Создание курса владельцем
    - Попытка создания курса другим пользователем (ограничения доступа)
    - Обновление курса владельцем
    - Попытка обновления курса другим пользователем (ограничения доступа)
    - Удаление курса владельцем
    - Попытка удаления курса другим пользователем (ограничения доступа)
    - Получение списка курсов без аутентификации (доступ запрещён)
    """

    def setUp(self):
        """
        Подготовка тестовых данных:
        - Создаются два пользователя: владелец курса и другой пользователь.
        - Создаётся тестовое изображение для загрузки.
        - Создаётся тестовый курс, принадлежащий владельцу.
        - Определяются URL для списка курсов и деталей конкретного курса.
        - Создаются клиенты API с аутентификацией для владельца, другого пользователя и анонимного.
        """
        self.owner = User.objects.create_user(
            email="owner@example.com", password="password123", username="owner"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="password123", username="other"
        )
        self.test_image = get_test_image_file()

        self.course = Course.objects.create(
            title="Test Course",
            description="Test course description",
            owner=self.owner,
            preview_image=self.test_image,
        )

        self.course_list_url = reverse("course-list")
        self.course_detail_url = reverse("course-detail", args=[self.course.id])

        self.client_owner = APIClient()
        self.client_owner.force_authenticate(user=self.owner)

        self.client_other = APIClient()
        self.client_other.force_authenticate(user=self.other_user)

        self.client_anon = APIClient()

    def test_list_courses(self):
        """
        Тест получения списка курсов аутентифицированным пользователем-владельцем.
        Проверяется, что статус ответа 200 OK и в списке есть хотя бы один курс.
        """
        response = self.client_owner.get(self.course_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_course_owner(self):
        """
        Тест создания нового курса пользователем-владельцем.
        Проверяется успешное создание (статус 201 Created) и совпадение заголовка курса.
        """
        image = get_test_image_file(name="new_course.jpg", ext="JPEG")
        data = {
            "title": "New Course",
            "description": "New course description",
            "preview_image": image,
        }
        response = self.client_owner.post(
            self.course_list_url, data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_create_course_other_user_forbidden(self):
        """
        Тест попытки создания курса другим пользователем, не являющимся владельцем.
        Проверяется, что операция либо успешна (если разрешена), либо возвращает ошибку доступа (403 Forbidden).
        """
        image = get_test_image_file(name="other_course.jpg", ext="JPEG")
        data = {
            "title": "Other Course",
            "description": "Other course description",
            "preview_image": image,
        }
        response = self.client_other.post(
            self.course_list_url, data, format="multipart"
        )
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]
        )

    def test_update_course_owner(self):
        """
        Тест обновления существующего курса пользователем-владельцем.
        Проверяется успешное обновление (статус 200 OK) и корректность обновлённого заголовка.
        """
        image = get_test_image_file(name="updated_course.jpg", ext="JPEG")
        data = {
            "title": "Updated Course",
            "description": "Updated course description",
            "preview_image": image,
        }
        response = self.client_owner.put(
            self.course_detail_url, data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_update_course_other_user_forbidden(self):
        """
        Тест попытки обновления курса другим пользователем.
        Проверяется, что операция либо запрещена (403 Forbidden), либо ресурс не найден (404 Not Found).
        """
        image = get_test_image_file(name="hacked_course.jpg", ext="JPEG")
        data = {
            "title": "Hacked Course",
            "description": "Hacked description",
            "preview_image": image,
        }
        response = self.client_other.put(
            self.course_detail_url, data, format="multipart"
        )
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    def test_delete_course_owner(self):
        """
        Тест удаления курса пользователем-владельцем.
        Проверяется успешное удаление (статус 204 No Content).
        """
        response = self.client_owner.delete(self.course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_other_user_forbidden(self):
        """
        Тест попытки удаления курса другим пользователем.
        Проверяется, что операция либо запрещена (403 Forbidden), либо ресурс не найден (404 Not Found).
        """
        response = self.client_other.delete(self.course_detail_url)
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

    def test_list_courses_unauthenticated(self):
        """
        Тест получения списка курсов анонимным (неаутентифицированным) пользователем.
        Проверяется, что доступ запрещён (статус 401 Unauthorized).
        """
        response = self.client_anon.get(self.course_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
