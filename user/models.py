from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator

## Kullanıcı yönetimi.
class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, surname, password, **extra_fields)
    
## Kullanıcı modeli.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, default='Default Name')
    surname = models.CharField(max_length=50, default='Default Surname')
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    discount_code = models.ForeignKey('order.DiscountCode', null=True, blank=True, on_delete=models.SET_NULL)  # Yeni alan

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return self.email
    
## Kullanıcının indirim kodunun tutulduğu model.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount_code = models.ForeignKey('order.DiscountCode', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email


## Kullanıcı ADRESİ modeli.
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

    def full_address(self):
        return f"{self.address}, {self.district}, {self.city}, {self.postal_code}"
    
    def __str__(self):
        return f"{self.title} - {self.address}, {self.district}, {self.city}"
    
