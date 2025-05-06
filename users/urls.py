from django.urls import path

from .views import (MyTokenObtainPairView, PaymentListView, RegisterView,
                    UserDetailView, UserListCreateView, UserProfileUpdateView)

urlpatterns = [
    path("profile/edit/", UserProfileUpdateView.as_view(), name="profile-edit"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
