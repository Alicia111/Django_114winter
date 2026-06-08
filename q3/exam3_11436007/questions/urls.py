from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('open/', views.question_open_list, name='question_open_list'),
    path('new/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('<int:pk>/manage/', views.question_manage, name='question_manage'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
