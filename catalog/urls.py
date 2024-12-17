from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home),
    path('<str:slug>/', views.category, name='category'),
]
