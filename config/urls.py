from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("lms.urls")),
    path("api/users/", include("users.urls")),
]
