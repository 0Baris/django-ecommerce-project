from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, default='Default Name')
    surname = models.CharField(max_length=50, default='Default Surname')
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return self.email
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Telefon numarası için kullanılması gereken format: '+999999999'.")],
        default='+900000000000'
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def full_address(self):
        return f"{self.address}, {self.district}, {self.city}, {self.postal_code}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Sipariş Alındı'),
        ('Processing', 'Hazırlanıyor'),
        ('Shipped', 'Kargolandı'),
        ('Delivered', 'Teslim Edildi'),
        ('Cancelled', 'İptal Edildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"