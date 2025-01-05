from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('management', views.account, name='account'),  # Hesap yönetimi
    path('orders', views.orders, name='orders'),  # Siparişler
    path('adresses', views.adress, name='adress'),  # Adresler
    path('add_address', views.add_address, name='add_address'),  # Adres ekle
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),  # Adres sil
    path('login', views.login_user, name='login'),  # Giriş yap
    path('logout', views.logout_user, name='logout'),  # Çıkış yap
    path('register', views.register_user, name='register'),  # Kayıt ol
    path('forgot-password', views.forgot_password, name='forgot-password'),  # Şifre hatırlatma bağlantısı

]