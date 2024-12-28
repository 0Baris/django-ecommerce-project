from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home),
    path('<str:slug>/', views.category, name='category'),
    path('products/<str:slug>/', views.product, name='product'),
]
