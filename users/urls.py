from django.urls import path

from .views import UserProfileUpdateView

urlpatterns = [
    path(
        "profile/edit/", UserProfileUpdateView.as_view(), name="profile-edit"
    ),  # Эндпоинт для редактирования профиля
]
