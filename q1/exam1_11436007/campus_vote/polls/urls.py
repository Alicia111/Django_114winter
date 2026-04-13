from django.urls import path

from . import views

urlpatterns = [
    path("", views.QuestionListView.as_view(), name="home"),
    path("question/<int:pk>/", views.question_detail, name="question_detail"),
    path("stats/", views.stats, name="stats"),
]
