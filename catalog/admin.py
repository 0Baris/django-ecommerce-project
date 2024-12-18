from django.contrib import admin
from .models import Category, Product, Slide

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'is_in_stock', 'is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku', 'category__name')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created_at', 'updated_at')
    search_fields = ('name', 'product__name')