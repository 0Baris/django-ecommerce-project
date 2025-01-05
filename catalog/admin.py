from django.contrib import admin
from .models import Category, Product, Slide, ProductImage, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'is_in_stock', 'is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku', 'category__name')
    inlines = [ProductImageInline]

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created_at', 'updated_at')
    search_fields = ('name', 'product__name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')