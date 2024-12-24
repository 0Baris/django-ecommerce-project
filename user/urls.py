from django.urls import path
from . import views

urlpatterns = [
    path('management', views.account, name='account'),
    path('orders', views.orders, name='orders'),
    path('adresses', views.adress, name='adress'),
    path('add_address', views.add_address, name='add_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('terms', views.terms, name='terms'),
]