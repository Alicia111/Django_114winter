from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("clubs/", views.clubs, name="clubs"),
    path("schedule/", views.ScheduleView.as_view(), name="schedule"),
    path("faq/", views.faq, name="faq"),
    path("about/", views.AboutView.as_view(), name="about"),
]
