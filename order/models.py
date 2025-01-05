from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from user.models import Address
import uuid


## İndirim Kodu için kullanılan model.
class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usage = models.PositiveIntegerField(default=0)
    usage_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.code

## Alışveriş Sepeti için kullanılan model.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
## Alışveriş sepetindeki ÜRÜNLER için kullanılan model.
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

## Sipariş için kullanılan model.
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Sipariş Alındı'),
        ('Processing', 'Hazırlanıyor'),
        ('Shipped', 'Kargolandı'),
        ('Delivered', 'Teslim Edildi'),
        ('Cancelled', 'İptal Edildi'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_code = models.ForeignKey(
        DiscountCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    def new_id(self):
        return self.id

    def __str__(self):
        return f"Sipariş/ ID:{self.id} , Satın Alan:{self.user.email}"
    
## Siparişteki ÜRÜNLER için kullanılan model.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} for Order {self.order.id}"

    def get_total_price(self):
        return self.quantity * self.price