from django.urls import path

from .views import SignUpView

# This app URL file only defines signup.
# Login and logout come from django.contrib.auth.urls.
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
