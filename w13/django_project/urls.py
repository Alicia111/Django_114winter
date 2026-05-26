from django.contrib import admin
from django.urls import include, path

from accounts.views import HomeView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", include("articles.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomeView.as_view(), name="home"),
]
