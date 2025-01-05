from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    ## Sepet yönlendirmeleri.
    path('cart/', views.view_cart, name='view_cart'),

    ## İndirim kodu  uygulanması.
    path('apply_discount/', views.apply_discount, name='apply_discount'),

    ## Sepet işlemleri.
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    ## Ödeme işlemi.
    path('checkout', views.checkout, name='checkout'),

]