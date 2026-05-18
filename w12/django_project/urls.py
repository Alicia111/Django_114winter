from django.contrib import admin
from django.urls import include, path

from accounts.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    # The local accounts.urls file only defines signup.
    path("accounts/", include("accounts.urls")),
    # Django provides built-in login and logout URLs.
    path("accounts/", include("django.contrib.auth.urls")),
    # The homepage now shows different content for logged-in users and roles.
    path("", HomeView.as_view(), name="home"),
]
