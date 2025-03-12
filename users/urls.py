from django.urls import path

from .views import PaymentListView, UserProfileUpdateView

urlpatterns = [
    path(
        "profile/edit/", UserProfileUpdateView.as_view(), name="profile-edit"
    ),  # Эндпоинт для редактирования профиля
    path("payments/", PaymentListView.as_view(), name="payment-list"),
]
