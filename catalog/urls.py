from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home),
    path('category/<int:id>/', views.category, name='category'),
]
