from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

## Kategori Modeli
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


## Ürün Modeli
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/img/products', )
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    mini_desc = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    comment_count = models.PositiveIntegerField(default=0)
    total_stars = models.PositiveIntegerField(default=0)

    @property
    def average_stars(self):
        if self.comment_count > 0:
            return self.total_stars / self.comment_count
        return 0

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.name, allow_unicode=True)
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(self.name, allow_unicode=True)}-{counter}"
                counter += 1
            self.slug = unique_slug

        if self.image:
            image = Image.open(self.image)
            max_size = (800, 800)
            if image.height > max_size[0] or image.width > max_size[1]:
                image.thumbnail(max_size, Image.LANCZOS)
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=85)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', f"{self.image.name.split('.')[0]}.jpg", 'image/jpeg', output.getbuffer().nbytes, None)

        super().save(*args, **kwargs)


## Slayt Modeli
class Slide(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='static/img/slides/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            image = Image.open(self.image)
            max_size = (1900, 600)
            if image.height > max_size[1] or image.width > max_size[0]:
                image.thumbnail(max_size, Image.LANCZOS)
            output = io.BytesIO()
            image.save(output, format='WEBP', quality=85)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', f"{self.image.name.split('.')[0]}.webp", 'image/webp', output.getbuffer().nbytes, None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


## Ürün Resmi Modeli
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/img/products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.image)
        max_size = (800, 800)

        if image.height > max_size[0] or image.width > max_size[1]:
            image.thumbnail(max_size, Image.LANCZOS)

        output = io.BytesIO()
        image.save(output, format='WEBP', quality=85)
        output.seek(0)

        webp_image_name = f"{self.image.name.split('.')[0]}.webp"

        self.image = InMemoryUploadedFile(
            output,
            'ImageField',
            webp_image_name,
            'image/webp',
            output.getbuffer().nbytes,
            None
        )

        super().save(*args, **kwargs)

        if not self.image_name:
            self.image_name = webp_image_name
            super().save(update_fields=['image_name'])


## Yorum Modeli
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"

    def save(self, *args, **kwargs):
        try:
            self.rating = int(self.rating)
        except ValueError:
            self.rating = 0

        if self.rating < 0:
            self.rating = 0
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)