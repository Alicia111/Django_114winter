from django.urls import path, include 

from .views import home_page_view

urlpatterns=[
        path("",home_page_view),]
